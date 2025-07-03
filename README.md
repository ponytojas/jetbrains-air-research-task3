# Stack Overflow Survey Analysis CLI Tool

A Python command-line tool and library for analyzing XLSX-based Stack Overflow Survey data. This tool provides interactive commands for exploring dataset structure, filtering respondents, analyzing answer distributions, and visualizing data with comprehensive test coverage.

## Features

- **Data Loading**: Load and validate XLSX survey files
- **Interactive CLI**: Command-line interface with help system
- **Data Analysis**: Filter respondents, analyze distributions, and generate statistics
- **Visualization**: Create charts and graphs from survey data
- **Library API**: Use as a Python library in your own projects
- **Full Test Coverage**: Comprehensive test suite with pytest

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. **Clone or download the project**:
   ```bash
   git clone <repository-url>
   cd task3
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Dependencies

The project requires the following packages:
- `pandas>=1.5.0` - Data manipulation and analysis
- `openpyxl>=3.0.0` - Excel file reading/writing
- `matplotlib>=3.5.0` - Data visualization
- `pytest>=7.0.0` - Testing framework
- `inquirer>=3.0.0` - Interactive command-line interfaces

## Usage

### Command Line Interface

#### Basic Usage

1. **Start the interactive CLI**:
   ```bash
   python main.py
   ```

2. **Load a survey file automatically**:
   ```bash
   python main.py path/to/your/survey.xlsx
   ```

3. **Get help**:
   ```bash
   python main.py --help
   ```

#### Interactive Commands

Once in the CLI, you can use these commands:

- `load <file_path>` - Load an XLSX survey file
- `list_questions` - Display all available survey questions
- `search <keyword>` - Search for questions containing a keyword
- `filter <conditions>` - Filter respondents based on criteria
- `distribution <question>` - Show answer distribution for a question
- `reset` - Reset all filters and return to original dataset
- `help` - Show available commands
- `exit` - Exit the application

#### Example Session

```bash
$ python main.py
Welcome to the Stack Overflow Survey Analysis Tool!
Type 'help' for available commands or 'help <command>' for specific help.
Start by loading a survey file with: load <path_to_xlsx_file>

survey> load survey_data.xlsx
Successfully loaded survey_data.xlsx with 1000 respondents and 50 questions.

survey> list_questions
Available questions:
1. Age
2. Country
3. Years of Experience
...

survey> search python
Found 3 questions matching 'python':
- PythonExperience
- PythonFrameworks
- PythonUsage

survey> distribution Country
Distribution for 'Country':
United States: 25.5%
Germany: 12.3%
United Kingdom: 8.7%
...

survey> exit
Goodbye!
```

### Using as a Library

You can also use the survey analysis tools as a Python library:

```python
from survey_tool import DataLoader, SurveyAnalyzer, SurveyVisualizer

# Load survey data
loader = DataLoader()
data = loader.load_excel("survey_data.xlsx")

# Analyze data
analyzer = SurveyAnalyzer(data)
filtered_data = analyzer.filter_respondents({"Country": "United States"})
distribution = analyzer.get_distribution("ProgrammingLanguage")

# Visualize results
visualizer = SurveyVisualizer()
visualizer.create_bar_chart(distribution, "Programming Language Usage")
```

#### Core Classes

- **`DataLoader`**: Handles loading and validating XLSX files
- **`SurveyAnalyzer`**: Provides data analysis and filtering capabilities
- **`SurveyVisualizer`**: Creates charts and visualizations
- **`SurveyCLI`**: Interactive command-line interface

## Testing

### Running Tests

The project includes a comprehensive test suite covering all major functionality.

1. **Run all tests**:
   ```bash
   python -m pytest
   ```

2. **Run tests with verbose output**:
   ```bash
   python -m pytest -v
   ```

3. **Run tests with coverage report**:
   ```bash
   python -m pytest --cov=survey_tool
   ```

4. **Run specific test file**:
   ```bash
   python -m pytest tests/test_data_loader.py
   ```

5. **Run tests for a specific function**:
   ```bash
   python -m pytest tests/test_analyzer.py::TestSurveyAnalyzer::test_filter_respondents
   ```

### Test Structure

The test suite is organized into three main test files:

- `tests/test_data_loader.py` - Tests for data loading functionality
- `tests/test_analyzer.py` - Tests for data analysis features
- `tests/test_visualizer.py` - Tests for visualization components

### Writing Tests

To add new tests, follow the existing patterns:

```python
import pytest
from survey_tool import DataLoader

class TestDataLoader:
    def test_load_valid_file(self):
        loader = DataLoader()
        # Test implementation
        assert loader.validate_file("valid_file.xlsx") is True
```

## Project Structure

```
task3/
├── main.py                 # Main entry point
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── survey_tool/           # Main package
│   ├── __init__.py        # Package initialization
│   ├── cli.py             # Command-line interface
│   ├── data_loader.py     # Data loading functionality
│   ├── analyzer.py        # Data analysis tools
│   └── visualizer.py      # Visualization components
├── tests/                 # Test suite
│   ├── __init__.py
│   ├── test_data_loader.py
│   ├── test_analyzer.py
│   └── test_visualizer.py
└── .venv/                 # Virtual environment (created locally)
```

## Development

### Setting Up Development Environment

1. **Clone the repository and set up environment**:
   ```bash
   git clone <repository-url>
   cd task3
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Run tests to verify setup**:
   ```bash
   python -m pytest
   ```

3. **Start developing**:
   ```bash
   python main.py
   ```

### Contributing

1. Ensure all tests pass before submitting changes
2. Follow the existing code style and patterns
3. Add tests for new functionality
4. Update documentation as needed

## Troubleshooting

### Common Issues

1. **"Module not found" errors**:
   - Ensure virtual environment is activated
   - Install dependencies: `pip install -r requirements.txt`

2. **Excel file loading errors**:
   - Verify file exists and is accessible
   - Check file format (must be .xlsx)
   - Ensure file is not corrupted

3. **Permission errors**:
   - Check file permissions
   - Ensure you have read access to the survey file

4. **Memory issues with large files**:
   - Monitor memory usage with large datasets
   - Consider processing data in chunks for very large files

## Version Information

- **Current Version**: 1.0.0
- **Python Compatibility**: 3.8+
- **Last Updated**: 2024

## License

This project is part of a development task and follows standard software development practices.