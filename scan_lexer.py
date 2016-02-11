import re
from collections import defaultdict

class Symbol:

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return str(self.name)

    def __eq__(self, a_string):
        return self.name == a_string


def bool_convert(value):
    return True if '#t' == value else False

def char_convert(value):
    char = str(value)
    return char

escape_dict={

           '\a':r'\a',
           '\b':r'\b',
           '\c':r'\c',
           '\f':r'\f',
           '\n':r'\n',
           '\r':r'\r',
           '\t':r'\t',
           '\v':r'\v',
           '\'':r'\'',
           '\"':r'\"',
           '\0':r'\0',
           '\1':r'\1',
           '\2':r'\2',
           '\3':r'\3',
           '\4':r'\4',
           '\5':r'\5',
           '\6':r'\6',
           '\8':r'\8',
           '\9':r'\9'
}

def raw(text):
    """Returns a raw string representation of text"""
    new_string=''
    for char in text:
        try: new_string+=escape_dict[char]
        except KeyError: new_string+=char
    return new_string

TOKEN_TYPES = (
    (bool_convert, re.compile('(#[tf])')),
    (char_convert,re.compile(r'#/(\w)')),
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

    line = raw(line)

    print(line)

    line = line.replace("\\",'/')

    print(line)

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
