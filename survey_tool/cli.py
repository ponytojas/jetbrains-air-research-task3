"""
Command-line interface module for the survey analysis tool.
Implements the interactive CLI using the cmd module.
"""

import cmd
import sys
import os
from typing import Optional, List
from .data_loader import DataLoader
from .analyzer import SurveyAnalyzer
from .visualizer import SurveyVisualizer


class SurveyCLI(cmd.Cmd):
    """Interactive command-line interface for survey analysis."""
    
    intro = """
Welcome to the Stack Overflow Survey Analysis Tool!
Type 'help' for available commands or 'help <command>' for specific help.
Start by loading a survey file with: load <path_to_xlsx_file>
"""
    
    prompt = "survey> "
    
    def __init__(self, file_path: Optional[str] = None):
        """
        Initialize the CLI.
        
        Args:
            file_path: Optional path to automatically load on startup
        """
        super().__init__()
        self.data_loader = DataLoader()
        self.analyzer = None
        self.visualizer = SurveyVisualizer()
        self.loaded_file = None
        
        # Auto-load file if provided
        if file_path:
            self.do_load(file_path)
    
    def do_load(self, file_path: str):
        """
        Load a survey XLSX file.
        
        Usage: load <path_to_xlsx_file>
        """
        if not file_path.strip():
            print("Error: Please provide a file path.")
            print("Usage: load <path_to_xlsx_file>")
            return
        
        try:
            self.data_loader.load_data(file_path.strip())
            self.analyzer = SurveyAnalyzer(self.data_loader)
            self.loaded_file = file_path.strip()
            
            print(f"Successfully loaded: {file_path}")
            print(f"Total respondents: {self.data_loader.get_total_respondents()}")
            print(f"Total questions: {len(self.data_loader.get_questions())}")
            
        except Exception as e:
            print(f"Error loading file: {str(e)}")
    
    def do_list_questions(self, args: str):
        """
        List all available questions in the dataset.
        
        Usage: list_questions
        """
        if not self._check_data_loaded():
            return
        
        questions = self.data_loader.get_questions()
        print(f"\nAvailable questions ({len(questions)}):")
        print("=" * 50)
        
        for i, question in enumerate(questions, 1):
            # Check if it's multiple choice
            mc_indicator = " (MC)" if self.data_loader.is_multiple_choice(question) else ""
            print(f"{i:3d}. {question}{mc_indicator}")
        
        print()
    
    def do_search(self, keyword: str):
        """
        Search for questions containing a keyword.
        
        Usage: search <keyword>
        """
        if not self._check_data_loaded():
            return
        
        if not keyword.strip():
            print("Error: Please provide a keyword to search for.")
            print("Usage: search <keyword>")
            return
        
        matches = self.data_loader.search_questions(keyword.strip())
        
        if matches:
            print(f"\nFound {len(matches)} question(s) matching '{keyword}':")
            print("=" * 50)
            
            for i, question in enumerate(matches, 1):
                mc_indicator = " (MC)" if self.data_loader.is_multiple_choice(question) else ""
                print(f"{i:3d}. {question}{mc_indicator}")
        else:
            print(f"No questions found matching '{keyword}'")
        
        print()
    
    def do_filter(self, args: str):
        """
        Filter respondents based on a question and option.
        
        Usage: filter <question>=<option>
        """
        if not self._check_data_loaded():
            return
        
        if not args.strip() or '=' not in args:
            print("Error: Invalid filter format.")
            print("Usage: filter <question>=<option>")
            print("Example: filter Age=25-34 years old")
            return
        
        try:
            question, option = args.split('=', 1)
            question = question.strip()
            option = option.strip()
            
            if not question or not option:
                print("Error: Both question and option must be provided.")
                return
            
            # Check if question exists
            if question not in self.data_loader.get_questions():
                print(f"Error: Question '{question}' not found.")
                print("Use 'list_questions' to see available questions.")
                return
            
            # Apply filter
            remaining = self.analyzer.filter_respondents(question, option)
            
            print(f"Filter applied: {question} = {option}")
            print(f"Remaining respondents: {remaining}")
            
            # Show active filters
            filters = self.analyzer.get_active_filters()
            if len(filters) > 1:
                print(f"Active filters: {len(filters)}")
                for q, o in filters.items():
                    print(f"  - {q} = {o}")
            
        except Exception as e:
            print(f"Error applying filter: {str(e)}")
    
    def do_distribution(self, question: str):
        """
        Show answer distribution for a question.
        
        Usage: distribution <question>
        """
        if not self._check_data_loaded():
            return
        
        if not question.strip():
            print("Error: Please provide a question name.")
            print("Usage: distribution <question>")
            return
        
        question = question.strip()
        
        if question not in self.data_loader.get_questions():
            print(f"Error: Question '{question}' not found.")
            print("Use 'list_questions' to see available questions.")
            return
        
        try:
            distribution = self.analyzer.get_distribution(question)
            
            if not distribution:
                print(f"No data available for question: {question}")
                return
            
            # Show terminal bar chart
            chart = self.visualizer.create_terminal_bar_chart(distribution, question)
            print(chart)
            
            # Show summary stats
            total_responses = sum(stats['count'] for stats in distribution.values())
            print(f"Total responses: {total_responses}")
            print(f"Unique answers: {len(distribution)}")
            
        except Exception as e:
            print(f"Error calculating distribution: {str(e)}")
    
    def do_chart(self, args: str):
        """
        Create a chart for a question distribution.
        
        Usage: chart <question> [format]
        Formats: terminal (default), matplotlib, table
        """
        if not self._check_data_loaded():
            return
        
        if not args.strip():
            print("Error: Please provide a question name.")
            print("Usage: chart <question> [format]")
            print("Formats: terminal (default), matplotlib, table")
            return
        
        parts = args.strip().split()
        question = parts[0]
        chart_format = parts[1] if len(parts) > 1 else 'terminal'
        
        if question not in self.data_loader.get_questions():
            print(f"Error: Question '{question}' not found.")
            return
        
        try:
            distribution = self.analyzer.get_distribution(question)
            
            if chart_format == 'terminal':
                chart = self.visualizer.create_terminal_bar_chart(distribution, question)
                print(chart)
            elif chart_format == 'matplotlib':
                result = self.visualizer.create_matplotlib_bar_chart(distribution, question)
                print(result)
            elif chart_format == 'table':
                table = self.visualizer.create_summary_table(distribution, question)
                print(table)
            else:
                print(f"Unknown format: {chart_format}")
                formats = self.visualizer.get_chart_formats()
                print("Available formats:")
                for fmt, desc in formats.items():
                    print(f"  - {fmt}: {desc}")
                
        except Exception as e:
            print(f"Error creating chart: {str(e)}")
    
    def do_reset(self, args: str):
        """
        Reset all filters and return to the original dataset.
        
        Usage: reset
        """
        if not self._check_data_loaded():
            return
        
        self.analyzer.reset_filters()
        print("All filters reset.")
        print(f"Total respondents: {self.data_loader.get_total_respondents()}")
    
    def do_status(self, args: str):
        """
        Show current status and summary statistics.
        
        Usage: status
        """
        if not self._check_data_loaded():
            return
        
        stats = self.analyzer.get_summary_stats()
        
        print("\n=== Survey Analysis Status ===")
        print(f"Loaded file: {self.loaded_file}")
        print(f"Total respondents: {stats['total_respondents']}")
        print(f"Total questions: {stats['total_questions']}")
        print(f"Active filters: {stats['active_filters']}")
        
        if stats['filter_details']:
            print("\nFilter details:")
            for question, option in stats['filter_details'].items():
                print(f"  - {question} = {option}")
        
        print()
    
    def do_options(self, question: str):
        """
        Show unique options/values for a specific question.
        
        Usage: options <question>
        """
        if not self._check_data_loaded():
            return
        
        if not question.strip():
            print("Error: Please provide a question name.")
            print("Usage: options <question>")
            return
        
        question = question.strip()
        
        if question not in self.data_loader.get_questions():
            print(f"Error: Question '{question}' not found.")
            return
        
        try:
            options = self.data_loader.get_unique_values(question)
            mc_indicator = " (Multiple Choice)" if self.data_loader.is_multiple_choice(question) else ""
            
            print(f"\nUnique options for: {question}{mc_indicator}")
            print("=" * min(len(question) + 20, 80))
            
            for i, option in enumerate(options, 1):
                print(f"{i:3d}. {option}")
            
            print(f"\nTotal unique options: {len(options)}")
            
        except Exception as e:
            print(f"Error getting options: {str(e)}")
    
    def do_exit(self, args: str):
        """
        Exit the survey analysis tool.
        
        Usage: exit
        """
        print("Thank you for using the Survey Analysis Tool!")
        return True
    
    def do_quit(self, args: str):
        """
        Quit the survey analysis tool.
        
        Usage: quit
        """
        return self.do_exit(args)
    
    def _check_data_loaded(self) -> bool:
        """Check if data has been loaded."""
        if self.data_loader.get_data() is None:
            print("Error: No data loaded. Use 'load <file_path>' to load a survey file.")
            return False
        return True
    
    def emptyline(self):
        """Handle empty line input."""
        pass
    
    def default(self, line: str):
        """Handle unknown commands."""
        print(f"Unknown command: {line}")
        print("Type 'help' for available commands.")
    
    def do_help(self, args: str):
        """Show help for commands."""
        if not args:
            print("\nAvailable commands:")
            print("==================")
            print("load <file>        - Load a survey XLSX file")
            print("list_questions     - List all questions in the dataset")
            print("search <keyword>   - Search for questions containing keyword")
            print("filter <q>=<opt>   - Filter respondents by question and option")
            print("distribution <q>   - Show answer distribution for a question")
            print("chart <q> [format] - Create a chart (terminal/matplotlib/table)")
            print("options <q>        - Show unique options for a question")
            print("reset              - Reset all filters")
            print("status             - Show current status and statistics")
            print("exit/quit          - Exit the tool")
            print("\nType 'help <command>' for detailed help on a specific command.")
        else:
            super().do_help(args)