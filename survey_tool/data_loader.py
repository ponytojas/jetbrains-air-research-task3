"""
Data loader module for handling XLSX files.
Handles loading Stack Overflow Survey data from Excel files.
"""

import pandas as pd
from typing import List, Dict, Any, Optional
import os


class DataLoader:
    """Handles loading and basic operations on XLSX survey data."""
    
    def __init__(self, file_path: Optional[str] = None):
        """
        Initialize the DataLoader.
        
        Args:
            file_path: Path to the XLSX file to load
        """
        self.file_path = file_path
        self.df = None
        self.original_df = None
        
    def load_data(self, file_path: str) -> pd.DataFrame:
        """
        Load data from an XLSX file.
        
        Args:
            file_path: Path to the XLSX file
            
        Returns:
            DataFrame with the loaded data
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            ValueError: If the file cannot be read or is empty
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        try:
            self.df = pd.read_excel(file_path, engine='openpyxl')
            self.original_df = self.df.copy()
            self.file_path = file_path
        except Exception as e:
            raise ValueError(f"Error reading file {file_path}: {str(e)}")
        
        if self.df.empty:
            raise ValueError(f"File {file_path} is empty or has no data")
        
        return self.df
    
    def get_questions(self) -> List[str]:
        """
        Get all questions (column headers) from the dataset.
        
        Returns:
            List of question/column names
        """
        if self.df is None:
            return []
        return self.df.columns.tolist()
    
    def search_questions(self, keyword: str) -> List[str]:
        """
        Search for questions containing a keyword.
        
        Args:
            keyword: The keyword to search for (case-insensitive)
            
        Returns:
            List of questions containing the keyword
        """
        if self.df is None:
            return []
        
        import re
        
        keyword_lower = keyword.lower()
        exact_matches = []
        partial_matches = []
        
        for col in self.df.columns:
            col_lower = col.lower()
            # Check for exact word match first
            pattern = r'\b' + re.escape(keyword_lower) + r'\b'
            if re.search(pattern, col_lower):
                exact_matches.append(col)
            # Check for partial match only if no exact match found yet
            elif keyword_lower in col_lower:
                partial_matches.append(col)
        
        # Return exact matches if found, otherwise partial matches
        return exact_matches if exact_matches else partial_matches
    
    def get_unique_values(self, question: str) -> List[str]:
        """
        Get unique values for a specific question.
        Handles both single-choice and multiple-choice questions.
        
        Args:
            question: The question/column name
            
        Returns:
            List of unique values for the question
        """
        if self.df is None or question not in self.df.columns:
            return []
        
        unique_values = set()
        
        for value in self.df[question].dropna():
            if isinstance(value, str) and ';' in value:
                # Multiple choice - split by semicolon
                for item in value.split(';'):
                    unique_values.add(item.strip())
            else:
                unique_values.add(str(value))
        
        return sorted(list(unique_values))
    
    def get_data(self) -> pd.DataFrame:
        """
        Get the current dataset.
        
        Returns:
            Current DataFrame
        """
        return self.df
    
    def reset_data(self):
        """Reset the dataset to its original state."""
        if self.original_df is not None:
            self.df = self.original_df.copy()
    
    def get_total_respondents(self) -> int:
        """
        Get the total number of respondents in the current dataset.
        
        Returns:
            Number of respondents
        """
        if self.df is None:
            return 0
        return len(self.df)
    
    def is_multiple_choice(self, question: str) -> bool:
        """
        Determine if a question is multiple choice based on semicolon-separated values.
        
        Args:
            question: The question/column name
            
        Returns:
            True if the question appears to be multiple choice
        """
        if self.df is None or question not in self.df.columns:
            return False
        
        # Check if any non-null values contain semicolons
        for value in self.df[question].dropna():
            if isinstance(value, str) and ';' in value:
                return True
        
        return False