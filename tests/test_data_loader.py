"""
Unit tests for the data_loader module.
Tests loading XLSX data, question operations, and utility functions.
"""

import pytest
import pandas as pd
import tempfile
import os
from unittest.mock import patch, MagicMock
from survey_tool.data_loader import DataLoader


class TestDataLoader:
    """Test cases for the DataLoader class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.loader = DataLoader()
        
        # Create sample test data
        self.test_data = pd.DataFrame({
            'Age': ['18-24 years old', '25-34 years old', '35-44 years old', '25-34 years old'],
            'Country': ['United States', 'Germany', 'United States', 'Canada'],
            'Languages': ['Python;JavaScript', 'Java;C++', 'Python', 'Python;JavaScript;Go'],
            'Experience': ['1-2 years', '5-9 years', '10-19 years', '3-5 years']
        })
    
    def create_temp_xlsx(self, data: pd.DataFrame) -> str:
        """Create a temporary XLSX file with test data."""
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx')
        data.to_excel(temp_file.name, index=False, engine='openpyxl')
        temp_file.close()
        return temp_file.name
    
    def test_init(self):
        """Test DataLoader initialization."""
        loader = DataLoader()
        assert loader.file_path is None
        assert loader.df is None
        assert loader.original_df is None
        
        loader_with_path = DataLoader('/some/path.xlsx')
        assert loader_with_path.file_path == '/some/path.xlsx'
    
    def test_load_data_success(self):
        """Test successful data loading."""
        temp_file = self.create_temp_xlsx(self.test_data)
        
        try:
            result = self.loader.load_data(temp_file)
            
            assert isinstance(result, pd.DataFrame)
            assert len(result) == 4
            assert list(result.columns) == ['Age', 'Country', 'Languages', 'Experience']
            assert self.loader.file_path == temp_file
            assert self.loader.df is not None
            assert self.loader.original_df is not None
            
        finally:
            os.unlink(temp_file)
    
    def test_load_data_file_not_found(self):
        """Test loading non-existent file."""
        with pytest.raises(FileNotFoundError):
            self.loader.load_data('/non/existent/file.xlsx')
    
    def test_load_data_invalid_file(self):
        """Test loading invalid file."""
        # Create a text file instead of XLSX
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.txt')
        temp_file.write(b'This is not an Excel file')
        temp_file.close()
        
        try:
            with pytest.raises(ValueError):
                self.loader.load_data(temp_file.name)
        finally:
            os.unlink(temp_file.name)
    
    def test_load_data_empty_file(self):
        """Test loading empty XLSX file."""
        empty_data = pd.DataFrame()
        temp_file = self.create_temp_xlsx(empty_data)
        
        try:
            with pytest.raises(ValueError):
                self.loader.load_data(temp_file)
        finally:
            os.unlink(temp_file)
    
    def test_get_questions_no_data(self):
        """Test getting questions when no data is loaded."""
        assert self.loader.get_questions() == []
    
    def test_get_questions_with_data(self):
        """Test getting questions with loaded data."""
        self.loader.df = self.test_data
        questions = self.loader.get_questions()
        
        expected = ['Age', 'Country', 'Languages', 'Experience']
        assert questions == expected
    
    def test_search_questions_no_data(self):
        """Test searching questions when no data is loaded."""
        assert self.loader.search_questions('age') == []
    
    def test_search_questions_case_insensitive(self):
        """Test case-insensitive question searching."""
        self.loader.df = self.test_data
        
        # Test different cases
        assert self.loader.search_questions('age') == ['Age']
        assert self.loader.search_questions('AGE') == ['Age']
        assert self.loader.search_questions('Age') == ['Age']
        
        # Test partial matches
        assert self.loader.search_questions('lang') == ['Languages']
        assert self.loader.search_questions('exp') == ['Experience']
    
    def test_search_questions_multiple_matches(self):
        """Test searching with multiple matches."""
        # Create data with multiple matching columns
        test_data = pd.DataFrame({
            'Programming Languages': ['Python'],
            'Spoken Languages': ['English'],
            'Age': ['25']
        })
        self.loader.df = test_data
        
        matches = self.loader.search_questions('language')
        assert len(matches) == 2
        assert 'Programming Languages' in matches
        assert 'Spoken Languages' in matches
    
    def test_search_questions_no_matches(self):
        """Test searching with no matches."""
        self.loader.df = self.test_data
        assert self.loader.search_questions('nonexistent') == []
    
    def test_get_unique_values_no_data(self):
        """Test getting unique values when no data is loaded."""
        assert self.loader.get_unique_values('Age') == []
    
    def test_get_unique_values_nonexistent_column(self):
        """Test getting unique values for non-existent column."""
        self.loader.df = self.test_data
        assert self.loader.get_unique_values('NonExistent') == []
    
    def test_get_unique_values_single_choice(self):
        """Test getting unique values for single-choice question."""
        self.loader.df = self.test_data
        values = self.loader.get_unique_values('Age')
        
        expected = ['18-24 years old', '25-34 years old', '35-44 years old']
        assert sorted(values) == sorted(expected)
    
    def test_get_unique_values_multiple_choice(self):
        """Test getting unique values for multiple-choice question."""
        self.loader.df = self.test_data
        values = self.loader.get_unique_values('Languages')
        
        expected = ['Python', 'JavaScript', 'Java', 'C++', 'Go']
        assert sorted(values) == sorted(expected)
    
    def test_get_unique_values_with_nan(self):
        """Test getting unique values with NaN values."""
        data_with_nan = self.test_data.copy()
        data_with_nan.loc[3, 'Age'] = None  # Replace duplicate value instead of unique one
        self.loader.df = data_with_nan
        
        values = self.loader.get_unique_values('Age')
        # NaN should be excluded
        assert len(values) == 3
        assert None not in values
    
    def test_get_data(self):
        """Test getting current dataset."""
        assert self.loader.get_data() is None
        
        self.loader.df = self.test_data
        result = self.loader.get_data()
        assert result is self.test_data
    
    def test_reset_data(self):
        """Test resetting data to original state."""
        temp_file = self.create_temp_xlsx(self.test_data)
        
        try:
            self.loader.load_data(temp_file)
            original_len = len(self.loader.df)
            
            # Modify current data
            self.loader.df = self.loader.df.head(2)
            assert len(self.loader.df) == 2
            
            # Reset
            self.loader.reset_data()
            assert len(self.loader.df) == original_len
            
        finally:
            os.unlink(temp_file)
    
    def test_reset_data_no_original(self):
        """Test resetting when no original data exists."""
        # Should not raise an error
        self.loader.reset_data()
        assert self.loader.df is None
    
    def test_get_total_respondents_no_data(self):
        """Test getting total respondents when no data is loaded."""
        assert self.loader.get_total_respondents() == 0
    
    def test_get_total_respondents_with_data(self):
        """Test getting total respondents with loaded data."""
        self.loader.df = self.test_data
        assert self.loader.get_total_respondents() == 4
    
    def test_is_multiple_choice_no_data(self):
        """Test checking multiple choice when no data is loaded."""
        assert self.loader.is_multiple_choice('Languages') == False
    
    def test_is_multiple_choice_nonexistent_column(self):
        """Test checking multiple choice for non-existent column."""
        self.loader.df = self.test_data
        assert self.loader.is_multiple_choice('NonExistent') == False
    
    def test_is_multiple_choice_single_choice(self):
        """Test identifying single-choice questions."""
        self.loader.df = self.test_data
        assert self.loader.is_multiple_choice('Age') == False
        assert self.loader.is_multiple_choice('Country') == False
    
    def test_is_multiple_choice_multiple_choice(self):
        """Test identifying multiple-choice questions."""
        self.loader.df = self.test_data
        assert self.loader.is_multiple_choice('Languages') == True
    
    def test_is_multiple_choice_mixed_data(self):
        """Test multiple choice detection with mixed data."""
        # Create data where some values have semicolons and some don't
        mixed_data = pd.DataFrame({
            'Mixed': ['Option1', 'Option2;Option3', 'Option4']
        })
        self.loader.df = mixed_data
        
        # Should be considered multiple choice if ANY value has semicolons
        assert self.loader.is_multiple_choice('Mixed') == True