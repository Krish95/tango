import pdb
from scan_lexer import Symbol
from functools import reduce
import operator


global_env = {
        "car"   : lambda x : x[0],
        "cdr"   : lambda x : x[1:],
        "max"   : max,
        "min"   : min,
        "+"     : lambda *x: reduce(operator.add, list(x)),
        "-"     : lambda *x: reduce(operator.sub, list(x))
        }


def atom(s):
    return not isinstance(s, list)

def istrue(exp):
    if exp == False:
        return False
    else:
        return True

def eprogn(exps, env):
    results = [evaluate(exp, env) for exp in exps]
    return results[-1]

def invoke(fn, arg_list):
    # pdb.set_trace()
    return fn(*arg_list)

def evlist(l, env):
    return [evaluate(x, env) for x in l]


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
        elif True in [isinstance(exp, x) for x in [int, float, str, bool]]:
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
        return eprogn(exp[1:], env)
    elif exp[0] == "set!":
        update(exp[1], env, evaluate(exp[2], env))
    elif exp[0] == "lambda":
        make_function(exp[1], exp[2:], env)

    # exp is function application
    else:
        return invoke(evaluate(exp[0], env), evlist(exp[1:], env))


def update(var, env, value):
    raise Exception("set! not implemented.")

def make_function(params, body):
    raise Exception("lambdas not implemented.")

