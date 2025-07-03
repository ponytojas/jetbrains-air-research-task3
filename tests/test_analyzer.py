"""
Unit tests for the analyzer module.
Tests filtering and distribution analysis functionality.
"""

import pytest
import pandas as pd
from unittest.mock import MagicMock
from survey_tool.data_loader import DataLoader
from survey_tool.analyzer import SurveyAnalyzer


class TestSurveyAnalyzer:
    """Test cases for the SurveyAnalyzer class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        # Create mock data loader with test data
        self.mock_loader = MagicMock(spec=DataLoader)
        
        # Create sample test data
        self.test_data = pd.DataFrame({
            'Age': ['18-24 years old', '25-34 years old', '35-44 years old', '25-34 years old'],
            'Country': ['United States', 'Germany', 'United States', 'Canada'],
            'Languages': ['Python;JavaScript', 'Java;C++', 'Python', 'Python;JavaScript;Go'],
            'Experience': ['1-2 years', '5-9 years', '10-19 years', '3-5 years']
        })
        
        self.mock_loader.get_data.return_value = self.test_data
        self.mock_loader.df = self.test_data
        self.analyzer = SurveyAnalyzer(self.mock_loader)
    
    def test_init(self):
        """Test SurveyAnalyzer initialization."""
        analyzer = SurveyAnalyzer(self.mock_loader)
        assert analyzer.data_loader is self.mock_loader
        assert analyzer.filters == {}
    
    def test_filter_respondents_no_data(self):
        """Test filtering when no data is loaded."""
        self.mock_loader.get_data.return_value = None
        
        with pytest.raises(ValueError, match="No data loaded"):
            self.analyzer.filter_respondents('Age', '25-34 years old')
    
    def test_filter_respondents_nonexistent_question(self):
        """Test filtering with non-existent question."""
        with pytest.raises(ValueError, match="Question 'NonExistent' not found"):
            self.analyzer.filter_respondents('NonExistent', 'some value')
    
    def test_filter_respondents_single_choice(self):
        """Test filtering single-choice questions."""
        # Mock the is_multiple_choice method
        self.mock_loader.is_multiple_choice.return_value = False
        
        result = self.analyzer.filter_respondents('Age', '25-34 years old')
        
        # Should filter to 2 respondents with that age
        assert result == 2
        assert self.analyzer.filters['Age'] == '25-34 years old'
        
        # Check that the dataloader's df was updated
        expected_df = self.test_data[self.test_data['Age'] == '25-34 years old']
        pd.testing.assert_frame_equal(self.mock_loader.df, expected_df)
    
    def test_filter_respondents_multiple_choice(self):
        """Test filtering multiple-choice questions."""
        # Mock the is_multiple_choice method
        self.mock_loader.is_multiple_choice.return_value = True
        
        result = self.analyzer.filter_respondents('Languages', 'Python')
        
        # Should filter to 3 respondents who know Python
        assert result == 3
        assert self.analyzer.filters['Languages'] == 'Python'
    
    def test_option_in_multiple_choice_with_semicolons(self):
        """Test checking option in semicolon-separated values."""
        assert self.analyzer._option_in_multiple_choice('Python;JavaScript', 'Python') == True
        assert self.analyzer._option_in_multiple_choice('Python;JavaScript', 'JavaScript') == True
        assert self.analyzer._option_in_multiple_choice('Python;JavaScript', 'Java') == False
        assert self.analyzer._option_in_multiple_choice('Python;JavaScript;Go', 'Go') == True
    
    def test_option_in_multiple_choice_single_value(self):
        """Test checking option in single values."""
        assert self.analyzer._option_in_multiple_choice('Python', 'Python') == True
        assert self.analyzer._option_in_multiple_choice('Python', 'Java') == False
    
    def test_option_in_multiple_choice_nan_value(self):
        """Test checking option with NaN values."""
        assert self.analyzer._option_in_multiple_choice(pd.NA, 'Python') == False
        assert self.analyzer._option_in_multiple_choice(None, 'Python') == False
    
    def test_option_in_multiple_choice_non_string(self):
        """Test checking option with non-string values."""
        assert self.analyzer._option_in_multiple_choice(123, '123') == True
        assert self.analyzer._option_in_multiple_choice(123, '456') == False
    
    def test_get_distribution_no_data(self):
        """Test getting distribution when no data is loaded."""
        self.mock_loader.get_data.return_value = None
        
        with pytest.raises(ValueError, match="No data loaded"):
            self.analyzer.get_distribution('Age')
    
    def test_get_distribution_nonexistent_question(self):
        """Test getting distribution for non-existent question."""
        with pytest.raises(ValueError, match="Question 'NonExistent' not found"):
            self.analyzer.get_distribution('NonExistent')
    
    def test_get_distribution_single_choice(self):
        """Test getting distribution for single-choice questions."""
        # Mock the is_multiple_choice method
        self.mock_loader.is_multiple_choice.return_value = False
        
        distribution = self.analyzer.get_distribution('Age')
        
        expected = {
            '25-34 years old': {'count': 2, 'percentage': 50.0},
            '18-24 years old': {'count': 1, 'percentage': 25.0},
            '35-44 years old': {'count': 1, 'percentage': 25.0}
        }
        
        assert distribution == expected
    
    def test_get_distribution_multiple_choice(self):
        """Test getting distribution for multiple-choice questions."""
        # Mock the is_multiple_choice method
        self.mock_loader.is_multiple_choice.return_value = True
        
        distribution = self.analyzer.get_distribution('Languages')
        
        # Python appears in 3 responses, JavaScript in 2, others in 1
        expected = {
            'Python': {'count': 3, 'percentage': 75.0},
            'JavaScript': {'count': 2, 'percentage': 50.0},
            'Java': {'count': 1, 'percentage': 25.0},
            'C++': {'count': 1, 'percentage': 25.0},
            'Go': {'count': 1, 'percentage': 25.0}
        }
        
        assert distribution == expected
    
    def test_get_single_choice_distribution(self):
        """Test _get_single_choice_distribution method."""
        distribution = self.analyzer._get_single_choice_distribution(
            self.test_data, 'Country', 4
        )
        
        expected = {
            'United States': {'count': 2, 'percentage': 50.0},
            'Germany': {'count': 1, 'percentage': 25.0},
            'Canada': {'count': 1, 'percentage': 25.0}
        }
        
        assert distribution == expected
    
    def test_get_multiple_choice_distribution(self):
        """Test _get_multiple_choice_distribution method."""
        distribution = self.analyzer._get_multiple_choice_distribution(
            self.test_data, 'Languages', 4
        )
        
        expected = {
            'Python': {'count': 3, 'percentage': 75.0},
            'JavaScript': {'count': 2, 'percentage': 50.0},
            'Java': {'count': 1, 'percentage': 25.0},
            'C++': {'count': 1, 'percentage': 25.0},
            'Go': {'count': 1, 'percentage': 25.0}
        }
        
        assert distribution == expected
    
    def test_get_multiple_choice_distribution_with_nan(self):
        """Test multiple choice distribution with NaN values."""
        data_with_nan = self.test_data.copy()
        data_with_nan.loc[3, 'Languages'] = None
        
        distribution = self.analyzer._get_multiple_choice_distribution(
            data_with_nan, 'Languages', 4
        )
        
        # Should skip NaN values
        expected = {
            'Python': {'count': 2, 'percentage': 50.0},
            'JavaScript': {'count': 1, 'percentage': 25.0},
            'Java': {'count': 1, 'percentage': 25.0},
            'C++': {'count': 1, 'percentage': 25.0}
        }
        
        assert distribution == expected
    
    def test_reset_filters(self):
        """Test resetting filters."""
        # Apply some filters first
        self.mock_loader.is_multiple_choice.return_value = False
        self.analyzer.filter_respondents('Age', '25-34 years old')
        self.analyzer.filter_respondents('Country', 'United States')
        
        assert len(self.analyzer.filters) == 2
        
        # Reset filters
        self.analyzer.reset_filters()
        
        assert self.analyzer.filters == {}
        self.mock_loader.reset_data.assert_called_once()
    
    def test_get_active_filters(self):
        """Test getting active filters."""
        # Initially no filters
        assert self.analyzer.get_active_filters() == {}
        
        # Apply some filters
        self.mock_loader.is_multiple_choice.return_value = False
        self.analyzer.filter_respondents('Age', '25-34 years old')
        self.analyzer.filter_respondents('Country', 'United States')
        
        filters = self.analyzer.get_active_filters()
        expected = {'Age': '25-34 years old', 'Country': 'United States'}
        assert filters == expected
        
        # Should return a copy, not the original
        filters['NewFilter'] = 'value'
        assert 'NewFilter' not in self.analyzer.filters
    
    def test_get_filtered_data(self):
        """Test getting filtered data."""
        result = self.analyzer.get_filtered_data()
        self.mock_loader.get_data.assert_called_once()
        assert result.equals(self.mock_loader.get_data.return_value)
    
    def test_get_summary_stats_no_data(self):
        """Test getting summary stats when no data is loaded."""
        self.mock_loader.get_data.return_value = None
        
        stats = self.analyzer.get_summary_stats()
        assert stats == {}
    
    def test_get_summary_stats_with_data(self):
        """Test getting summary stats with data."""
        # Apply some filters
        self.mock_loader.is_multiple_choice.return_value = False
        self.analyzer.filter_respondents('Age', '25-34 years old')
        
        stats = self.analyzer.get_summary_stats()
        
        expected = {
            'total_respondents': 4,
            'total_questions': 4,
            'active_filters': 1,
            'filter_details': {'Age': '25-34 years old'}
        }
        
        assert stats == expected
    
    def test_multiple_filters(self):
        """Test applying multiple filters sequentially."""
        self.mock_loader.is_multiple_choice.return_value = False
        
        # Apply first filter
        self.analyzer.filter_respondents('Age', '25-34 years old')
        assert len(self.analyzer.filters) == 1
        
        # Apply second filter - should override the dataloader's df
        filtered_df = self.test_data[self.test_data['Age'] == '25-34 years old']
        self.mock_loader.get_data.return_value = filtered_df
        self.mock_loader.df = filtered_df
        
        self.analyzer.filter_respondents('Country', 'United States')
        assert len(self.analyzer.filters) == 2
        
        expected_filters = {'Age': '25-34 years old', 'Country': 'United States'}
        assert self.analyzer.filters == expected_filters