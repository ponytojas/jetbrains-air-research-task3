#!/usr/bin/env python3
"""
Main entry point for the Stack Overflow Survey Analysis CLI Tool.

This script provides the command-line interface for analyzing XLSX-based
Stack Overflow Survey data with interactive commands for exploration,
filtering, and visualization.
"""

import sys
import argparse
from survey_tool.cli import SurveyCLI


def main():
    """Main function to start the survey analysis CLI."""
    parser = argparse.ArgumentParser(
        description="Stack Overflow Survey Analysis CLI Tool",
        epilog="Interactive commands: load, list_questions, search, filter, distribution, reset, exit"
    )
    
    parser.add_argument(
        "file", 
        nargs="?", 
        help="Path to the XLSX survey file to load automatically"
    )
    
    parser.add_argument(
        "--version", 
        action="version", 
        version="Survey Analysis Tool 1.0.0"
    )
    
    args = parser.parse_args()
    
    try:
        # Initialize and start the CLI
        cli = SurveyCLI(file_path=args.file)
        cli.cmdloop()
        
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()