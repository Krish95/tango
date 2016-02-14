
import scan_lexer,evaluator
import readline

class REPL:

    def __init__(self):

        #self.scope = 
        self.init_history()
        self.init_completer()

    def init_history(self):
        import os, atexit

        histfile = os.path.join(os.path.expanduser("~"), ".pyschemehistory")

        try:
            readline.read_history_file(histfile)
        except IOError:
            pass

        atexit.register(readline.write_history_file, histfile)

    def init_completer(self):
        readline.parse_and_bind("tab: complete")#"tab: complete" on Linux
        readline.set_completer_delims(' ')
        readline.set_completer(self.completer)

    def roll(self):
        stored_tokens = []

        while True:
            try:
                line = input("py-scheme>> ").strip()
            except EOFError:
                print
                break

            if not line:
                continue

            try:
                tokens = scan_lexer.tokenize(line)
            except Exception as e:
                print(e)
                continue

            stored_tokens += tokens

            ast, balance = scan_lexer.prstree_balance(stored_tokens)

            if balance > 0:
                continue
            elif balance < 0:
                print('Unexpected ")"')
                stored_tokens = []
                continue

            stored_tokens = []

            for expr in ast:
               # Print the evaluation of the expression in scope.evaluate(expression)
               print(evaluator.evaluate(expr))

    def completer(self, input, state):
        tokens = scan_lexer.tokenize(input)

        symbol = tokens[-1]

        if not scan_lexer.is_smbl(symbol):
            return None

        options = self.get_options(symbol.name)

        if state >= len(options):
            return None

        tokens[-1] = options[state]

        return ''.join(tokens)

    @staticmethod
    #add scope attrib
    def get_options(name):
        """Supply known_names in the present scope add the variables present too.
        After adding Scope."""

        known_names = ["quote","if","begin","set","lambda"]

        return [var for var in known_names if var.startswith(name)]
