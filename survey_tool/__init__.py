"""
Stack Overflow Survey Analysis CLI Tool

A command-line library for analyzing XLSX-based Stack Overflow Survey data.
Supports exploring dataset structure, filtering respondents, analyzing answer distributions,
and visualizing data with full test coverage.
"""

from .data_loader import DataLoader
from .analyzer import SurveyAnalyzer
from .cli import SurveyCLI
from .visualizer import SurveyVisualizer

__version__ = "1.0.0"
__author__ = "Survey Analysis Team"

__all__ = [
    "DataLoader",
    "SurveyAnalyzer", 
    "SurveyCLI",
    "SurveyVisualizer"
]