import pandas as pd
from survey_tool.explorer import SurveyExplorer

def test_list_and_search():
    df = pd.DataFrame({"Q1": ["A"], "Q2": ["B"]})
    explorer = SurveyExplorer(df)
    assert set(explorer.list_questions()) == {"Q1", "Q2"}
    assert explorer.search_questions("Q1") == ["Q1"]
    assert explorer.search_questions("q") == ["Q1", "Q2"]

def test_unique_values():
    df = pd.DataFrame({"Q1": ["A;B", "B;C", "A"]})
    explorer = SurveyExplorer(df)
    assert set(explorer.unique_values("Q1")) == {"A", "B", "C"}
