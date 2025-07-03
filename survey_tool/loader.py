import pandas as pd

class SurveyLoader:
    @staticmethod
    def load_xlsx(file_path):
        return pd.read_excel(file_path, engine='openpyxl')
