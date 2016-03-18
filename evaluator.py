import pdb
from scan_lexer import Symbol
from global_env import *

macros = {}
scope = []

def evaluate(exp, envs = [global_env]):

    #Use the global scope list
    global scope

    # Is exp an atom?
    if atom(exp):
        if type(exp) == Symbol:
           return lookup(exp, envs)
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
        if istrue(evaluate(exp[1], envs)):
            return evaluate(exp[2], envs)
        else:
            return evaluate(exp[3], envs)
    elif exp[0] == "begin":
        return eprogn(exp[1:], envs)
    elif exp[0] == "set!":
        update(exp[1], envs, evaluate(exp[2], envs))
    elif exp[0] == "define":
        envs[0].insert(0, (exp[1], evaluate(exp[2], envs)))
    elif exp[0] == "lambda":
        return make_function(exp[1], exp[2:], envs)
    elif exp[0] == "macro":
        return (exp[1], exp[2])
    # exp is a macro expansion
    elif type(evaluate(exp[0], envs)) == tuple:
        f = evaluate(exp[0], envs)
        # pdb.set_trace()
        expanded_form = macro_expand(f[0], exp[1:], f[1], envs)
        return evaluate(evaluate(expanded_form, envs), envs)
    # exp is function application
    else:
        return invoke(evaluate(exp[0], envs), evlist(exp[1:], envs))

    #Preserve current scope
    scope = [str(inner[0]) for outer in envs for inner in outer]


def macro_expand(variables, values, body, envs):
    if len(variables) != len(values):
        raise ValueError("Too few or too many values.")
    def substitute(exp):
        nonlocal variables, values
        if atom(exp):
            if exp in variables:
                return [Symbol("quote"), values[variables.index(exp)]]
            else:
                return exp
        else:
            return [substitute(e) for e in exp]

    result = [substitute(exp) for exp in body]
    return result

def istrue(exp):
    if exp == False:
        return False
    else:
        return True

def eprogn(exps, envs):
    results = [evaluate(exp, envs) for exp in exps]
    return results[-1]

def invoke(fn, arg_list):
    # pdb.set_trace()
    return fn(*arg_list)

def evlist(l, envs):
    return [evaluate(x, envs) for x in l]

# update is impure.
def update(var, envs, value):
    # pdb.set_trace()
    for i in range(len(envs)):
        for j in range(len(envs[i])):
            if envs[i][j][0] == var:
                envs[i][j] = (var, value)
                return
    raise Exception("No such Symbol found: ", var)

def make_function(variables, body, envs):
    return lambda *values : evaluate(body[0], extend(envs, variables, list(values)))


def lookup(var, envs):
    for env in envs: 
        for u, v in env:
            if u == var:
                return v
    raise Exception("No such binding: ", var)

def extend(envs, variables, values):
    if len(variables) != len(values):
        raise ValueError("Too few or too many values.")
    else:
        bindings = list(zip(variables, values))
        new_envs = [bindings]
        for env in envs:
            new_envs.append(env)
        return new_envs







