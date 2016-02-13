from scan_lexer import *
from evaluator import *
import pdb

def read_form():
    unmatched_parantheses = 0
    lines = ""
    while True:
        line = input()
        lines = lines + line
        unmatched_parantheses = unmatched_parantheses + line.count("(")
        unmatched_parantheses = unmatched_parantheses - line.count(")")
        if unmatched_parantheses == 0:
            return lines



def repl():
    while True:
        print('> ', end="")
        lines = read_form()
        # pdb.set_trace()
        ast, error = prstree_balance(tokenize(lines))
        assert error == 0
        ast = ast[0]    # Potential Problem?
        try:
            print(ast, " => ", evaluate(ast))
        except:
            print("Evaluation failed.")




if __name__ == "__main__":
    repl()


