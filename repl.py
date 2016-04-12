
import scan_lexer,evaluator
import readline
import re,pdb,sys     
from global_env import *

class REPL:

    def __init__(self):

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
        readline.parse_and_bind("tab: complete") #"tab: complete" on Linux
        readline.set_completer_delims(' ')
        readline.set_completer(self.completer)

    def roll(self):
    
        while True:
            
            try:
                line = read_form()
            except (KeyboardInterrupt,EOFError) as e:
                print("\nMoriturus te saluto.")
                exit(0)

            tokens = scan_lexer.tokenize(line)

            balance = 0

            ast,balance = scan_lexer.prstree_balance(tokens)

            if balance < 0:
                print("Exception: Cannot close more than opened parentheses")
                continue
            elif balance > 0:
                print("Exception: All opened parentheses must be closed")
                continue

            """ Replacing the string format"""
            ast = str_format(ast)    

            for expr in ast:
                """ Print the evaluation of the expression in scope.evaluate(expression) """
                try:                    
                    print(evaluator.evaluate(expr))
                except Exception as e:
                    print(str(e))


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

        known_names = ["quote","if","begin","set!","lambda","define","macro","exit","load"] + [str(x[0]) for x in global_env]
        known_names.extend(evaluator.scope)

        return [var for var in known_names if var.startswith(name)]

def read_form():

    unmatched_parantheses = 0
    lines = ""
    line = input("=>")
    while True:
        lines = lines + line.rstrip("/")
        if line.endswith("/"):
            lines = lines + ' '
            line = input("... ") 
        else:
            return lines   

def str_format(ast):
      re_str = re.compile('(\..*?\.)')
      for l in ast:
            ind_out = ast.index(l)
            if isinstance(l,list):
                  ast[ind_out]=str_format(l)
            elif scan_lexer.is_str(l):
                  ast[ind_out]= str(l).strip('\.')  
      return ast      

