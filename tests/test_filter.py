import pandas as pd
from survey_tool.filter import SurveyFilter

def test_filter_sc():
    df = pd.DataFrame({"Q1": ["A", "B", "A"]})
    f = SurveyFilter(df)
    f.apply_filter("Q1", "A")
    filtered = f.get_filtered()
    assert all(filtered["Q1"] == "A")

def test_filter_mc():
    df = pd.DataFrame({"Q1": ["A;B", "B;C", "A"]})
    f = SurveyFilter(df)
    f.apply_filter("Q1", "B")
    filtered = f.get_filtered()
    assert set(filtered["Q1"]) == {"A;B", "B;C"}

def test_reset():
    df = pd.DataFrame({"Q1": ["A", "B"]})
    f = SurveyFilter(df)
    f.apply_filter("Q1", "A")
    f.reset()
    assert f.get_filtered().shape == (2, 1)
