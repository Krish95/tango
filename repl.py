
import scan_lexer,evaluator
import readline
import re,pdb

def read_form():

    unmatched_parantheses = 0
    lines = ""
    print("=>",end="")
    while True:
        line = input()
        lines = lines + line
        if line.endswith("/"):
            lines = lines + ' '
            print("... ",end="")  
        else:
            return lines   

def str_format(ast):
      re_str = re.compile('(\..*?\.)')
      for l in ast:
            ind_out = ast.index(l)
            if isinstance(l,list):
                  ast[ind_out]=str_format(l)
            elif scan_lexer.is_str(l):
                  ind_in = ast[ind_out].index(x)
                  ast[ind_out][ind_in] = str(x).strip('\.')  
      return ast           

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
        #pdb.set_trace()
        while True:
            
            line = read_form()

            try:
                tokens = scan_lexer.tokenize(line)
            except Exception as e:
                print(e)
                continue

            stored_tokens += tokens

            ast = scan_lexer.prstree_balance(stored_tokens)

            # if balance > 0:
            #     continue
            # elif balance < 0:
            #     print('Unexpected ")"')
            #     stored_tokens = []
            #     continue

            """ Replacing the string format"""
            # re_str = re.compile('(\..*?\.)')
            # for l in ast:
            # 	ind_out = ast.index(l)
            # 	if isinstance(l,list):
            # 		for x in l:
            # 			if scan_lexer.is_str(x):
            # 				ind_in = ast[ind_out].index(x)
            # 				ast[ind_out][ind_in] = str(x).strip('\.')
            # 	elif scan_lexer.is_str(l):
            # 		ind_in = ast[ind_out].index(x)
            # 		ast[ind_out][ind_in] = str(x).strip('\.')   
            ast = str_format(ast)        

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

        known_names = ["quote","if","begin","set!","lambda"]

        return [var for var in known_names if var.startswith(name)]
