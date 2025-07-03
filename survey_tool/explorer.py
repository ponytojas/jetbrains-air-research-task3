class SurveyExplorer:
    def __init__(self, df):
        self.df = df

    def list_questions(self):
        return list(self.df.columns)

    def search_questions(self, keyword):
        keyword = keyword.lower()
        return [col for col in self.df.columns if keyword in col.lower()]

    def unique_values(self, question):
        if question in self.df.columns:
            values = set()
            for val in self.df[question].dropna():
                if isinstance(val, str):
                    for v in val.split(';'):
                        values.add(v.strip())
                else:
                    values.add(val)
            return sorted(values)
        return []
