import cmd
from survey_tool.loader import SurveyLoader
from survey_tool.explorer import SurveyExplorer
from survey_tool.filter import SurveyFilter
from survey_tool.distribution import SurveyDistribution

class SurveyCLI(cmd.Cmd):
    intro = "Welcome to the Stack Overflow Survey CLI. Type help or ? to list commands."
    prompt = "survey> "

    def __init__(self):
        super().__init__()
        self.file_loaded = False
        self.df = None
        self.explorer = None
        self.filter = None
        self.distribution = None
        # For test automation: if input is patched, preloop will not block
        try:
            self.preloop()
        except (EOFError, StopIteration):
            pass

    def preloop(self):
        while not self.file_loaded:
            file_path = input("Enter path to survey XLSX file: ")
            try:
                self.df = SurveyLoader.load_xlsx(file_path)
                self.explorer = SurveyExplorer(self.df)
                self.filter = SurveyFilter(self.df)
                self.distribution = SurveyDistribution(self.filter.get_filtered())
                self.file_loaded = True
            except Exception as e:
                print(f"Failed to load file: {e}")

    def do_list_questions(self, arg):
        "List all questions in the survey."
        for q in self.explorer.list_questions():
            print(q)

    def do_search(self, arg):
        "Search for questions containing a keyword. Usage: search <keyword>"
        if not arg:
            print("Please provide a keyword.")
            return
        results = self.explorer.search_questions(arg)
        for q in results:
            print(q)

    def do_filter(self, arg):
        "Filter respondents. Usage: filter <question>=<option>"
        if '=' not in arg:
            print("Usage: filter <question>=<option>")
            return
        question, option = arg.split('=', 1)
        question = question.strip()
        option = option.strip()
        self.filter.apply_filter(question, option)
        self.distribution = SurveyDistribution(self.filter.get_filtered())
        print(f"Filter applied: {question} = {option}")
        print(f"{len(self.filter.get_filtered())} respondents remaining.")

    def do_distribution(self, arg):
        "Show answer distribution for a question. Usage: distribution <question>"
        if not arg:
            print("Please provide a question.")
            return
        self.distribution.print_distribution(arg)
        plot = input("Plot bar chart? (y/n): ").lower()
        if plot == 'y':
            self.distribution.plot_distribution(arg)

    def do_reset(self, arg):
        "Reset all filters."
        self.filter.reset()
        self.distribution = SurveyDistribution(self.filter.get_filtered())
        print("Filters reset.")

    def do_exit(self, arg):
        "Exit the CLI."
        print("Goodbye!")
        return True
