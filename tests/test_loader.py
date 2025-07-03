import pandas as pd
from survey_tool.loader import SurveyLoader

def test_load_xlsx(tmp_path):
    file = tmp_path / "test.xlsx"
    df = pd.DataFrame({"Q1": ["A", "B"]})
    df.to_excel(file, index=False)
    loaded = SurveyLoader.load_xlsx(file)
    assert list(loaded.columns) == ["Q1"]
    assert loaded.shape == (2, 1)
