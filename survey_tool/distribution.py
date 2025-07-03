import pandas as pd
import matplotlib.pyplot as plt

class SurveyDistribution:
    def __init__(self, df):
        self.df = df

    def get_distribution(self, question):
        if question not in self.df.columns:
            return {}
        counts = {}
        total = 0
        for val in self.df[question].dropna():
            if isinstance(val, str):
                for v in val.split(';'):
                    v = v.strip()
                    counts[v] = counts.get(v, 0) + 1
                    total += 1
            else:
                counts[val] = counts.get(val, 0) + 1
                total += 1
        return counts, total

    def print_distribution(self, question):
        counts, total = self.get_distribution(question)
        for k, v in sorted(counts.items(), key=lambda x: -x[1]):
            pct = 100 * v / total if total else 0
            print(f"{k}: {v} ({pct:.2f}%)")

    def plot_distribution(self, question):
        counts, total = self.get_distribution(question)
        if not counts:
            print("No data to plot.")
            return
        plt.figure(figsize=(10, 5))
        plt.bar(counts.keys(), counts.values())
        plt.title(f"Distribution for: {question}")
        plt.ylabel("Count")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()
