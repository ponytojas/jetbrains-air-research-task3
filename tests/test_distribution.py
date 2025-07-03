import pandas as pd
from survey_tool.distribution import SurveyDistribution

def test_distribution_sc():
    df = pd.DataFrame({"Q1": ["A", "B", "A"]})
    d = SurveyDistribution(df)
    counts, total = d.get_distribution("Q1")
    assert counts["A"] == 2
    assert counts["B"] == 1
    assert total == 3

def test_distribution_mc():
    df = pd.DataFrame({"Q1": ["A;B", "B;C", "A"]})
    d = SurveyDistribution(df)
    counts, total = d.get_distribution("Q1")
    assert counts["A"] == 2
    assert counts["B"] == 2
    assert counts["C"] == 1
    assert total == 5
