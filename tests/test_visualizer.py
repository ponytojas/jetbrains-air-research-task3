"""
Unit tests for the visualizer module.
Tests chart creation and visualization functionality.
"""

import pytest
import tempfile
import os
from unittest.mock import patch, MagicMock
from survey_tool.visualizer import SurveyVisualizer


class TestSurveyVisualizer:
    """Test cases for the SurveyVisualizer class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.visualizer = SurveyVisualizer()
        
        # Sample distribution data for testing
        self.distribution_data = {
            'Python': {'count': 100, 'percentage': 40.0},
            'JavaScript': {'count': 75, 'percentage': 30.0},
            'Java': {'count': 50, 'percentage': 20.0},
            'C++': {'count': 25, 'percentage': 10.0}
        }
        
        self.empty_distribution = {}
        
        self.large_distribution = {
            f'Option{i}': {'count': 100 - i*5, 'percentage': (100 - i*5)/100 * 100}
            for i in range(25)
        }
    
    def test_init(self):
        """Test SurveyVisualizer initialization."""
        visualizer = SurveyVisualizer()
        assert visualizer is not None
    
    def test_create_terminal_bar_chart_success(self):
        """Test creating a terminal bar chart with valid data."""
        result = self.visualizer.create_terminal_bar_chart(
            self.distribution_data, "Programming Languages"
        )
        
        assert isinstance(result, str)
        assert "Distribution for: Programming Languages" in result
        assert "Python" in result
        assert "JavaScript" in result
        assert "100" in result  # Count
        assert "40.0" in result  # Percentage
        assert "█" in result  # Bar character
    
    def test_create_terminal_bar_chart_empty_data(self):
        """Test creating terminal bar chart with empty data."""
        result = self.visualizer.create_terminal_bar_chart(
            self.empty_distribution, "Empty Question"
        )
        
        assert "No data available for question: Empty Question" in result
    
    def test_create_terminal_bar_chart_sorting(self):
        """Test that terminal bar chart sorts by count descending."""
        result = self.visualizer.create_terminal_bar_chart(
            self.distribution_data, "Languages"
        )
        
        lines = result.split('\n')
        data_lines = [line for line in lines if 'Python' in line or 'JavaScript' in line or 'Java' in line or 'C++' in line]
        
        # Python should appear before JavaScript (higher count)
        python_idx = next(i for i, line in enumerate(data_lines) if 'Python' in line)
        js_idx = next(i for i, line in enumerate(data_lines) if 'JavaScript' in line)
        assert python_idx < js_idx
    
    def test_create_terminal_bar_chart_max_width(self):
        """Test terminal bar chart with custom max width."""
        result = self.visualizer.create_terminal_bar_chart(
            self.distribution_data, "Languages", max_width=20
        )
        
        # Check that bars are present and properly sized
        assert "█" in result
        # With max_width=20, Python (100 count) should have 20 bars, JavaScript (75) should have 15
        lines = result.split('\n')
        python_line = next(line for line in lines if 'Python' in line)
        js_line = next(line for line in lines if 'JavaScript' in line)
        
        # Count bars in each line
        python_bars = python_line.count('█')
        js_bars = js_line.count('█')
        
        assert python_bars == 20  # 100/100 * 20 = 20
        assert js_bars == 15  # 75/100 * 20 = 15
    
    def test_create_terminal_bar_chart_long_option_names(self):
        """Test terminal bar chart with long option names."""
        long_name_data = {
            'Very Long Programming Language Name That Exceeds Normal Length': {'count': 50, 'percentage': 50.0},
            'Short': {'count': 50, 'percentage': 50.0}
        }
        
        result = self.visualizer.create_terminal_bar_chart(
            long_name_data, "Languages"
        )
        
        # Long names should be truncated
        assert "Very Long Programming Language..." in result
        assert "Short" in result
    
    @patch('matplotlib.pyplot.savefig')
    @patch('matplotlib.pyplot.close')
    @patch('matplotlib.pyplot.tight_layout')
    @patch('matplotlib.pyplot.text')
    @patch('matplotlib.pyplot.xticks')
    @patch('matplotlib.pyplot.ylabel')
    @patch('matplotlib.pyplot.xlabel')
    @patch('matplotlib.pyplot.title')
    @patch('matplotlib.pyplot.bar')
    @patch('matplotlib.pyplot.figure')
    def test_create_matplotlib_bar_chart_success(self, mock_figure, mock_bar, mock_title, 
                                                mock_xlabel, mock_ylabel, mock_xticks, 
                                                mock_text, mock_tight_layout, mock_close, mock_savefig):
        """Test creating matplotlib chart with valid data."""
        # Mock the bar return value
        mock_bars = [MagicMock() for _ in range(4)]
        for i, bar in enumerate(mock_bars):
            bar.get_x.return_value = i
            bar.get_width.return_value = 1
            bar.get_height.return_value = [100, 75, 50, 25][i]
        mock_bar.return_value = mock_bars
        
        result = self.visualizer.create_matplotlib_bar_chart(
            self.distribution_data, "Programming Languages"
        )
        
        # Check that matplotlib functions were called
        mock_figure.assert_called_once()
        mock_bar.assert_called_once()
        mock_title.assert_called_once()
        mock_savefig.assert_called_once()
        mock_close.assert_called_once()
        
        assert "Chart saved to:" in result
        assert ".png" in result
    
    @patch('matplotlib.pyplot.savefig')
    @patch('matplotlib.pyplot.close')
    def test_create_matplotlib_bar_chart_with_output_path(self, mock_close, mock_savefig):
        """Test creating matplotlib chart with custom output path."""
        with patch('matplotlib.pyplot.figure'), \
             patch('matplotlib.pyplot.bar'), \
             patch('matplotlib.pyplot.title'), \
             patch('matplotlib.pyplot.xlabel'), \
             patch('matplotlib.pyplot.ylabel'), \
             patch('matplotlib.pyplot.xticks'), \
             patch('matplotlib.pyplot.text'), \
             patch('matplotlib.pyplot.tight_layout'):
            
            output_path = "/tmp/test_chart.png"
            result = self.visualizer.create_matplotlib_bar_chart(
                self.distribution_data, "Languages", output_path=output_path
            )
            
            mock_savefig.assert_called_with(output_path, dpi=300, bbox_inches='tight')
            assert f"Chart saved to: {output_path}" in result
    
    def test_create_matplotlib_bar_chart_empty_data(self):
        """Test creating matplotlib chart with empty data."""
        result = self.visualizer.create_matplotlib_bar_chart(
            self.empty_distribution, "Empty Question"
        )
        
        assert "No data available for question: Empty Question" in result
    
    @patch('matplotlib.pyplot.savefig')
    @patch('matplotlib.pyplot.close')
    def test_create_matplotlib_bar_chart_top_n(self, mock_close, mock_savefig):
        """Test matplotlib chart with top_n parameter."""
        with patch('matplotlib.pyplot.figure'), \
             patch('matplotlib.pyplot.bar') as mock_bar, \
             patch('matplotlib.pyplot.title'), \
             patch('matplotlib.pyplot.xlabel'), \
             patch('matplotlib.pyplot.ylabel'), \
             patch('matplotlib.pyplot.xticks'), \
             patch('matplotlib.pyplot.text'), \
             patch('matplotlib.pyplot.tight_layout'):
            
            # Mock bar chart with expected number of bars
            mock_bars = [MagicMock() for _ in range(10)]
            for i, bar in enumerate(mock_bars):
                bar.get_x.return_value = i
                bar.get_width.return_value = 1
                bar.get_height.return_value = 100 - i*5
            mock_bar.return_value = mock_bars
            
            result = self.visualizer.create_matplotlib_bar_chart(
                self.large_distribution, "Languages", top_n=10
            )
            
            # Should only plot top 10 items
            call_args = mock_bar.call_args
            assert len(call_args[0][1]) == 10  # counts array should have 10 items
            assert "Chart saved to:" in result
    
    def test_create_summary_table_success(self):
        """Test creating summary table with valid data."""
        result = self.visualizer.create_summary_table(
            self.distribution_data, "Programming Languages"
        )
        
        assert isinstance(result, str)
        assert "Top 4 answers for: Programming Languages" in result
        assert "Option" in result
        assert "Count" in result
        assert "Percentage" in result
        assert "Python" in result
        assert "100" in result
        assert "40.0%" in result
    
    def test_create_summary_table_empty_data(self):
        """Test creating summary table with empty data."""
        result = self.visualizer.create_summary_table(
            self.empty_distribution, "Empty Question"
        )
        
        assert "No data available for question: Empty Question" in result
    
    def test_create_summary_table_top_n(self):
        """Test summary table with top_n parameter."""
        result = self.visualizer.create_summary_table(
            self.distribution_data, "Languages", top_n=2
        )
        
        assert "Top 2 answers for: Languages" in result
        assert "Python" in result
        assert "JavaScript" in result
        # Java and C++ should not be included
        assert "Java" not in result or result.count("Java") <= 1  # Might appear in header
        assert "C++" not in result
    
    def test_create_summary_table_sorting(self):
        """Test that summary table sorts by count descending."""
        result = self.visualizer.create_summary_table(
            self.distribution_data, "Languages"
        )
        
        lines = result.split('\n')
        data_lines = [line for line in lines if any(lang in line for lang in ['Python', 'JavaScript', 'Java', 'C++'])]
        
        # Remove lines that might contain language names in headers
        data_lines = [line for line in data_lines if any(str(count) in line for count in [100, 75, 50, 25])]
        
        if len(data_lines) >= 2:
            # Python should appear before JavaScript
            assert 'Python' in data_lines[0]
            assert 'JavaScript' in data_lines[1]
    
    def test_create_summary_table_long_option_names(self):
        """Test summary table with long option names."""
        long_name_data = {
            'Very Long Programming Language Name That Exceeds Normal Length': {'count': 50, 'percentage': 50.0},
            'Short': {'count': 50, 'percentage': 50.0}
        }
        
        result = self.visualizer.create_summary_table(
            long_name_data, "Languages"
        )
        
        # Long names should be truncated
        assert "Very Long Programming Language Name..." in result
        assert "Short" in result
    
    def test_get_chart_formats(self):
        """Test getting available chart formats."""
        formats = self.visualizer.get_chart_formats()
        
        assert isinstance(formats, dict)
        assert 'terminal' in formats
        assert 'matplotlib' in formats
        assert 'table' in formats
        
        # Check descriptions
        assert 'Terminal-based bar chart' in formats['terminal']
        assert 'PNG chart using matplotlib' in formats['matplotlib']
        assert 'Formatted table summary' in formats['table']
    
    def test_create_terminal_bar_chart_zero_counts(self):
        """Test terminal bar chart with zero counts."""
        zero_data = {
            'Option1': {'count': 0, 'percentage': 0.0},
            'Option2': {'count': 0, 'percentage': 0.0}
        }
        
        result = self.visualizer.create_terminal_bar_chart(zero_data, "Zero Question")
        
        # Should handle zero counts gracefully
        assert "Distribution for: Zero Question" in result
        assert "Option1" in result
        assert "Option2" in result
        # Should not have any bar characters for zero counts
        lines = result.split('\n')
        data_lines = [line for line in lines if 'Option' in line and ('0.0%' in line or '0 ' in line)]
        for line in data_lines:
            # Should have no bars for zero counts
            bars_in_line = line.count('█')
            assert bars_in_line == 0