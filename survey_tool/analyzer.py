"""
Survey analyzer module for filtering and distribution analysis.
Handles filtering respondents and calculating answer distributions.
"""

import pandas as pd
from typing import List, Dict, Any, Tuple
from .data_loader import DataLoader


class SurveyAnalyzer:
    """Handles filtering and analysis of survey data."""
    
    def __init__(self, data_loader: DataLoader):
        """
        Initialize the analyzer with a data loader.
        
        Args:
            data_loader: DataLoader instance with loaded data
        """
        self.data_loader = data_loader
        self.filters = {}
        
    def filter_respondents(self, question: str, option: str) -> int:
        """
        Filter respondents based on a question and option.
        Handles both single-choice and multiple-choice questions.
        
        Args:
            question: The question/column name to filter by
            option: The option value to filter for
            
        Returns:
            Number of respondents after filtering
            
        Raises:
            ValueError: If question doesn't exist in dataset
        """
        df = self.data_loader.get_data()
        
        if df is None:
            raise ValueError("No data loaded")
        
        if question not in df.columns:
            raise ValueError(f"Question '{question}' not found in dataset")
        
        # Store the filter
        self.filters[question] = option
        
        # Apply the filter
        if self.data_loader.is_multiple_choice(question):
            # Multiple choice - check if option is in semicolon-separated values
            mask = df[question].apply(
                lambda x: self._option_in_multiple_choice(x, option)
            )
        else:
            # Single choice - exact match
            mask = df[question] == option
        
        # Apply the filter
        self.data_loader.df = df[mask].copy()
        
        return len(self.data_loader.df)
    
    def _option_in_multiple_choice(self, value: Any, option: str) -> bool:
        """
        Check if an option exists in a multiple-choice value.
        
        Args:
            value: The value to check (could be string with semicolons or other)
            option: The option to look for
            
        Returns:
            True if option is found in the value
        """
        if pd.isna(value):
            return False
        
        value_str = str(value)
        if ';' in value_str:
            # Split by semicolon and check each part
            parts = [part.strip() for part in value_str.split(';')]
            return option in parts
        else:
            # Single value
            return value_str == option
    
    def get_distribution(self, question: str) -> Dict[str, Dict[str, Any]]:
        """
        Get answer distribution for a question.
        
        Args:
            question: The question/column name to analyze
            
        Returns:
            Dictionary with distribution statistics including counts and percentages
            
        Raises:
            ValueError: If question doesn't exist in dataset
        """
        df = self.data_loader.get_data()
        
        if df is None:
            raise ValueError("No data loaded")
        
        if question not in df.columns:
            raise ValueError(f"Question '{question}' not found in dataset")
        
        total_respondents = len(df)
        
        if self.data_loader.is_multiple_choice(question):
            return self._get_multiple_choice_distribution(df, question, total_respondents)
        else:
            return self._get_single_choice_distribution(df, question, total_respondents)
    
    def _get_single_choice_distribution(self, df: pd.DataFrame, question: str, total: int) -> Dict[str, Dict[str, Any]]:
        """Get distribution for single-choice questions."""
        value_counts = df[question].value_counts()
        
        distribution = {}
        for value, count in value_counts.items():
            distribution[str(value)] = {
                'count': int(count),
                'percentage': round((count / total) * 100, 2)
            }
        
        return distribution
    
    def _get_multiple_choice_distribution(self, df: pd.DataFrame, question: str, total: int) -> Dict[str, Dict[str, Any]]:
        """Get distribution for multiple-choice questions."""
        option_counts = {}
        
        # Count occurrences of each option
        for value in df[question].dropna():
            if isinstance(value, str) and ';' in value:
                # Multiple values
                for option in value.split(';'):
                    option = option.strip()
                    option_counts[option] = option_counts.get(option, 0) + 1
            else:
                # Single value
                option = str(value)
                option_counts[option] = option_counts.get(option, 0) + 1
        
        # Convert to distribution format
        distribution = {}
        for option, count in option_counts.items():
            distribution[option] = {
                'count': count,
                'percentage': round((count / total) * 100, 2)
            }
        
        return distribution
    
    def reset_filters(self):
        """Reset all filters and restore original dataset."""
        self.filters = {}
        self.data_loader.reset_data()
    
    def get_active_filters(self) -> Dict[str, str]:
        """
        Get currently active filters.
        
        Returns:
            Dictionary of active filters {question: option}
        """
        return self.filters.copy()
    
    def get_filtered_data(self) -> pd.DataFrame:
        """
        Get the currently filtered dataset.
        
        Returns:
            Filtered DataFrame
        """
        return self.data_loader.get_data()
    
    def get_summary_stats(self) -> Dict[str, Any]:
        """
        Get summary statistics for the current dataset.
        
        Returns:
            Dictionary with summary statistics
        """
        df = self.data_loader.get_data()
        
        if df is None:
            return {}
        
        return {
            'total_respondents': len(df),
            'total_questions': len(df.columns),
            'active_filters': len(self.filters),
            'filter_details': self.filters
        }