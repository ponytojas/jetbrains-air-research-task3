# Stack Overflow Survey Analysis CLI Tool

## Installation

```
pip install -r requirements.txt
```

## Usage

```
python main.py
```

You will be prompted to enter the path to your Stack Overflow survey XLSX file.

## Features
- List all questions
- Search questions
- Filter respondents
- Show answer distributions (with optional bar chart)
- Reset filters

## Run Tests

```
pytest
```

## Project Structure

- `main.py`: CLI entry point
- `survey_tool/`: Library code
- `tests/`: Unit tests

## Notes
- The tool expects the first row of the XLSX file to contain headers/questions.
- Multi-choice answers should be semicolon-separated.
