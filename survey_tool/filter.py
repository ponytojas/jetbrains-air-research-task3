import pandas as pd

class SurveyFilter:
    def __init__(self, df):
        self.original_df = df.copy()
        self.df = df.copy()
        self.filters = []

    def apply_filter(self, question, option):
        if question not in self.df.columns:
            return
        def match(val):
            if pd.isna(val):
                return False
            if isinstance(val, str):
                return option in [v.strip() for v in val.split(';')]
            return val == option
        self.df = self.df[self.df[question].apply(match)]
        self.filters.append((question, option))

    def reset(self):
        self.df = self.original_df.copy()
        self.filters = []

    def get_filtered(self):
        return self.df
