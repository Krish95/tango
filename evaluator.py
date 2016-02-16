import pdb
from scan_lexer import Symbol
from functools import reduce
import operator


global_env = [
        ("car"   , lambda x : x[0]) ,
        ("cdr"   , lambda x : x[1:]) ,
        ("max"   , max) ,
        ("min"   , min) ,
        ("+"     , lambda *x: reduce(operator.add, list(x))) ,
        ("-"     , lambda *x: reduce(operator.sub, list(x)))
]


def evaluate(exp, env = global_env):
    #pdb.set_trace()
    # Is exp an atom?
    if atom(exp):
        if type(exp) == Symbol:
           return lookup(exp, env)
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
        return make_function(exp[1], exp[2:], env)

    # exp is function application
    else:
        return invoke(evaluate(exp[0], env), evlist(exp[1:], env))


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

# update is impure.
def update(var, env, value):
    # pdb.set_trace()
    for i in range(len(env)):
        if env[i][0] == var:
            env[i] = (var, value)
            return
    raise Exception("No such symbol found: ", var)
        
def make_function(variables, body, env):
    return lambda *values : evaluate(body[0], extend(env, variables, list(values)))

def lookup(var, env):
    for u, v in env:
        if u == var:
            return v
    raise Exception("No such binding: ", var)

def extend(env, variables, values):
    if len(variables) != len(values):
        raise ValueError("Too few or too many values.")
    else:
        bindings = list(zip(variables, values))
        return bindings + env





