from functools import reduce
import operator

def atom(s):
    return not isinstance(s, list)

global_env = [
        ("car"   , lambda x : x[0]) ,
        ("cdr"   , lambda x : x[1:]) ,
        ("cons"  , lambda h,t : [h] + t),
        ("max"   , max) ,
        ("min"   , min) ,
        ("+"     , lambda *x: reduce(operator.add, list(x))) ,
        ("-"     , lambda *x: reduce(operator.sub, list(x))),
        ("*"     , lambda *x: reduce(operator.mul, list(x))),
        ("/"     , lambda *x: reduce(operator.truediv, list(x))),
        ("<"     , lambda *x: reduce(operator.lt, list(x))),
        (">"     , lambda *x: reduce(operator.gt, list(x))),
        ("<="    , lambda *x: reduce(operator.le, list(x))),
        (">="    , lambda *x: reduce(operator.ge, list(x))),
        ("="     , lambda *x: reduce(operator.eq, list(x))),
        ("length", len),
        ("null?" , lambda x: x == []),
        ("atom?" , atom),
        ("list?" , lambda x: not atom(x)),

]


