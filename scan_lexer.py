import re
from collections import defaultdict

class Symbol:

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return str(self.name)


def bool_convert(value):
    return True if '#t' == value else False

TOKEN_TYPES = (
    (bool_convert, re.compile('(#[tf])')),
    (float, re.compile('((0|[1-9]+[0-9]*)\.[0-9]+)')),
    (int, re.compile('(0|[1-9]+[0-9]*)')),
    (str, re.compile('"([^"]*)"')),
    (Symbol, re.compile('([^\(\)\'"\s]+)')),
)

def find_atom(line, tokens):

    if line.startswith(';'):
        return ''

    for atom in ['(', ')', "'"]:
        if line.startswith(atom):
            tokens.append(atom)
            return line[len(atom):]

    return None

def find_token(line, tokens):
    for cast, pattern in TOKEN_TYPES:
        r = pattern.match(line);
        if not r:
            continue

        tokens.append(cast(r.group(1)))

        return line[len(r.group(0)):]

    return None

def _tokenize(line, tokens):
    line = line.lstrip()

    if len(line) == 0:
        return

    r = find_atom(line, tokens)
    
    if None != r:
        _tokenize(r, tokens)
        return

    r = find_token(line, tokens)
    
    if None != r:
        _tokenize(r, tokens)
        return

    raise Exception("Failed tokenizing: %s" % line)

def tokenize(line):
    tokens = []
    _tokenize(line, tokens)
    return tokens

def tokenize_from_file(fname):
    line_num = 0
    tokens = []
    for line in open(fname).read().splitlines():
        line_num += 1

        try:
            _tokenize(line, tokens)
        except:
            raise Exception("Lexer-Error on Line %d: \n%s" % (line_num, line))

    return tokens

def prstree_balance(tokens):

    lists = defaultdict(list)
    i = 0
    depth = 0

    while i < len(tokens):
        if '(' == tokens[i]:
            depth += 1
        elif ')' == tokens[i]:
            lists[depth-1].append(lists[depth])
            del(lists[depth])
            depth -= 1
        else:
            lists[depth].append(tokens[i])

        i += 1

    return (lists[0], depth)
