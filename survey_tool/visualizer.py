"""
Visualizer module for creating charts and visual representations.
Handles both terminal-based and matplotlib-based visualizations.
"""

import matplotlib.pyplot as plt
from typing import Dict, Any, Optional
import os


class SurveyVisualizer:
    """Handles visualization of survey data distributions."""
    
    def __init__(self):
        """Initialize the visualizer."""
        pass
    
    def create_terminal_bar_chart(self, distribution: Dict[str, Dict[str, Any]], 
                                 question: str, max_width: int = 50) -> str:
        """
        Create a terminal-based bar chart for distribution data.
        
        Args:
            distribution: Distribution data from analyzer
            question: Question name for the chart title
            max_width: Maximum width of bars in characters
            
        Returns:
            String representation of the bar chart
        """
        if not distribution:
            return f"No data available for question: {question}"
        
        # Sort by count descending
        sorted_items = sorted(distribution.items(), 
                            key=lambda x: x[1]['count'], 
                            reverse=True)
        
        # Find the maximum count for scaling
        max_count = max(item[1]['count'] for item in sorted_items)
        
        # Build the chart
        chart_lines = []
        chart_lines.append(f"\nDistribution for: {question}")
        chart_lines.append("=" * min(len(question) + 20, 80))
        
        for option, stats in sorted_items:
            count = stats['count']
            percentage = stats['percentage']
            
            # Calculate bar width
            if max_count > 0:
                bar_width = int((count / max_count) * max_width)
            else:
                bar_width = 0
            
            # Create the bar
            bar = "█" * bar_width
            
            # Truncate long option names
            display_option = option[:30] + "..." if len(option) > 30 else option
            
            # Format the line
            line = f"{display_option:35} {bar} {count:6} ({percentage:5.1f}%)"
            chart_lines.append(line)
        
        chart_lines.append("")
        return "\n".join(chart_lines)
    
    def create_matplotlib_bar_chart(self, distribution: Dict[str, Dict[str, Any]], 
                                   question: str, output_path: Optional[str] = None,
                                   top_n: int = 20) -> str:
        """
        Create a matplotlib bar chart for distribution data.
        
        Args:
            distribution: Distribution data from analyzer
            question: Question name for the chart title
            output_path: Path to save the chart (optional)
            top_n: Number of top answers to show
            
        Returns:
            Path to the saved chart or status message
        """
        if not distribution:
            return f"No data available for question: {question}"
        
        # Sort by count descending and take top N
        sorted_items = sorted(distribution.items(), 
                            key=lambda x: x[1]['count'], 
                            reverse=True)[:top_n]
        
        # Extract data for plotting
        labels = [item[0] for item in sorted_items]
        counts = [item[1]['count'] for item in sorted_items]
        
        # Create the plot
        plt.figure(figsize=(12, 8))
        bars = plt.bar(range(len(labels)), counts)
        
        # Customize the plot
        plt.title(f"Distribution: {question}", fontsize=14, fontweight='bold')
        plt.xlabel("Options", fontsize=12)
        plt.ylabel("Count", fontsize=12)
        
        # Set x-axis labels
        plt.xticks(range(len(labels)), labels, rotation=45, ha='right')
        
        # Add value labels on bars
        for bar, count in zip(bars, counts):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                    str(count), ha='center', va='bottom')
        
        # Adjust layout to prevent label cutoff
        plt.tight_layout()
        
        # Save or show the plot
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()
            return f"Chart saved to: {output_path}"
        else:
            # Generate a default filename
            safe_question = "".join(c for c in question if c.isalnum() or c in (' ', '-', '_')).strip()
            safe_question = safe_question.replace(' ', '_')[:50]
            filename = f"survey_chart_{safe_question}.png"
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            plt.close()
            return f"Chart saved to: {filename}"
    
    def create_summary_table(self, distribution: Dict[str, Dict[str, Any]], 
                           question: str, top_n: int = 10) -> str:
        """
        Create a formatted table summary of distribution data.
        
        Args:
            distribution: Distribution data from analyzer
            question: Question name for the table title
            top_n: Number of top answers to show
            
        Returns:
            String representation of the summary table
        """
        if not distribution:
            return f"No data available for question: {question}"
        
        # Sort by count descending
        sorted_items = sorted(distribution.items(), 
                            key=lambda x: x[1]['count'], 
                            reverse=True)[:top_n]
        
        # Build the table
        table_lines = []
        table_lines.append(f"\nTop {min(top_n, len(sorted_items))} answers for: {question}")
        table_lines.append("=" * min(len(question) + 30, 80))
        
        # Header
        table_lines.append(f"{'Option':<40} {'Count':<10} {'Percentage':<10}")
        table_lines.append("-" * 60)
        
        # Data rows
        for option, stats in sorted_items:
            count = stats['count']
            percentage = stats['percentage']
            
            # Truncate long option names
            display_option = option[:35] + "..." if len(option) > 35 else option
            
            line = f"{display_option:<40} {count:<10} {percentage:.1f}%"
            table_lines.append(line)
        
        table_lines.append("")
        return "\n".join(table_lines)
    
    def get_chart_formats(self) -> Dict[str, str]:
        """
        Get available chart formats.
        
        Returns:
            Dictionary of format names and descriptions
        """
        return {
            'terminal': 'Terminal-based bar chart',
            'matplotlib': 'PNG chart using matplotlib',
            'table': 'Formatted table summary'
        }