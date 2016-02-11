import pdb
from scan_lexer import Symbol

global_env = {
        "car"   : lambda x : x[0],
        "cdr"   : lambda x : x[1:]
        }

atom_types = [int, float, str, bool ]

def atom(s):
    return not isinstance(s, list)

def istrue(exp):
    if exp == False:
        return False
    else:
        return True

def evaluate(exp, env = global_env):
    # pdb.set_trace()
    # Is exp an atom?
    if atom(exp):
        if type(exp) == Symbol:
            try:
                return global_env[str(exp)]
            except KeyError:
                print("No such Symbol found.")
                return None
        elif True in map(lambda x: isinstance(exp, x), atom_types):
            return exp
        else:
            raise TypeError("Unknown type atom", exp)

    # Is exp the null list?
    if exp == []:
        return []

    # Is exp is a special form?
    elif exp[0] == "quote":
        return exp[1]
    elif exp[0] == "if":
        if istrue(evaluate(exp[1], env)):
            return evaluate(exp[2], env)
        else:
            return evaluate(exp[3], env)
    elif exp[0] == "begin":
        eprogn(exp[1], env)
    elif exp[0] == "set!":
        update(exp[1], env, evaluate(exp[2], env))
    elif exp[0] == "lambda":
        make_function(exp[1], exp[2:], env)

    # exp is function application
    else:
        invoke(evaluate(exp[0], env), evlis(exp[1:], env))
