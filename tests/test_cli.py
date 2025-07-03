import pytest
from survey_tool.cli import SurveyCLI

# CLI tests would require mocking input/output, which can be done with pytest's monkeypatch fixture.
def test_cli_list_questions(monkeypatch):
    import builtins
    import pandas as pd
    from survey_tool.loader import SurveyLoader
    from survey_tool.explorer import SurveyExplorer
    from survey_tool.filter import SurveyFilter
    from survey_tool.distribution import SurveyDistribution

    # Patch input to provide a fake file path and then exit
    inputs = iter(["tests/test.xlsx", "exit"])
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))

    # Patch SurveyLoader to load a dummy DataFrame
    monkeypatch.setattr(SurveyLoader, "load_xlsx", lambda _: pd.DataFrame({"Q1": ["A", "B"]}))

    cli = SurveyCLI()
    cli.onecmd("list_questions")
