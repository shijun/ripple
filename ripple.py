#!/usr/bin/env python

from ply.lex import TOKEN

tokens = [
    'ATOM',
    'STRING',
    'QUOTE',
    'BOOL',
    'NUMBER',
]

# An atom is a letter or symbol, followed by
# any number of letters, digits, or symbols.
symbol = r'[!$%&|*+-/:<=>?@^_~]'
identifier = r'([A-Za-z]|%s)' % symbol + r'(\w|%s)*' % symbol
t_ATOM = identifier

t_STRING = r'"(\\[abtnvfr"\\\W]|[^\\"])*"'

t_QUOTE = r"'"

def t_BOOL(t):
    r'\#[tf]'
    if t.value == '#t':
        t.value = True
    else: # t.value == '#f'
        t.value = False
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_ignore = ' \t\n'

literals = '()'

def t_error(t):
    print('Illegal character: %s' % t.value[0])
    t.lexer.skip(1)

import ply.lex as lex
lexer = lex.lex()

def evaluate(expression, bindings):
    if   isinstance(expression, str): # variable
        return bindings[expression]
    elif isinstance(expression, int):
        return expression

    if expression[0] == 'define':
        if isinstance(expression[1], list):
            # defining a function
            name = expression[1][0]
            function = dict()
            function['parameters'] = expression[1][1:]
            function['body'] = expression[2:]
            bindings[name] = function
        else:
            # defining a variable
            bindings[expression[1]] = expression[2]
        return None

    if expression[0] == 'if':
        predicate = expression[1]
        consequence = expression[2]
        alternative = expression[3]

        if evaluate(predicate, bindings) == '#t':
            return evaluate(consequence, bindings)
        else:
            return evaluate(alternative, bindings)

    if expression[0] == 'quote':
        tail = [str(item) for item in expression[1:]]
        return '({0})'.format(' '.join(tail))

    # User-defined functions and primitives are below.
    # Their parameters are evaluated.
    head = expression[0]
    tail = [evaluate(item, bindings) for item in expression[1:]]

    # Call the function if it's defined by the user.
    if head in bindings:
        function = bindings[head]
        arguments = zip(function['parameters'], tail)

        from copy import deepcopy
        closure = deepcopy(bindings)
        closure.update(arguments)

        result = None
        for statement in function['body']:
            result = evaluate(statement, closure)
        return result

    # primitives
    from functools import reduce
    from operator import add, sub, mul, div

    if   head == '+':
        return reduce(add, tail)
    elif head == '-':
        return reduce(sub, tail)
    elif head == '*':
        return reduce(mul, tail)
    elif head == '/':
        return reduce(div, tail)
    elif head == '=':
        return '#t' if tail[0] == tail[1] else '#f'
    elif head == '>':
        return '#t' if tail[0] > tail[1] else '#f'
    elif head == '<':
        return '#t' if tail[0] < tail[1] else '#f'

toplevel = dict()

def p_expression(p):
    '''expression : expression list
                  | empty'''
    if len(p) == 3:
        p[0] = evaluate(p[2], toplevel)
    else:
        p[0] = p[1]

def p_expression_single(p):
    '''expression : terminal
                  | quote'''
    p[0] = evaluate(p[1], toplevel)

def p_list(p):
    '''list : '(' elements ')' '''
    p[0] = p[2]

def p_quote(p):
    '''quote : QUOTE '(' elements ')' '''
    p[0] = ['quote'] + p[3]

def p_elements(p):
    '''elements : elements terminal
                | elements list
                | empty'''
    # the following is a left unfold [i.e. opposite of foldl()]
    if len(p) == 3:
        if p[1] is None: # at the beginning of the list
            p[1] = []
        p[0] = p[1] + [p[2]]

def p_terminal(p):
    '''terminal : BOOL
                | STRING
                | NUMBER
                | ATOM'''
    p[0] = p[1]

def p_empty(p):
    '''empty :'''
    pass

def p_error(p):
    print('Syntax error: %s' % p.value)

import ply.yacc as yacc
yacc.yacc()

def parse(program):
    """Parse a valid Scheme program.

    >>> parse('terminal.scm')
    42

    >>> parse('simple.scm')
    4

    >>> parse('many-terms.scm')
    372

    >>> parse('variable.scm')
    10

    >>> parse('quote.scm')
    '(3 2 1)'

    >>> parse('function.scm')
    14

    >>> parse('parameters.scm')
    6

    >>> parse('equal.scm')
    '#f'

    >>> parse('if.scm')
    9

    >>> parse('factorial.scm')
    120
    """

    with open(program) as file:
        return yacc.parse(file.read())

if __name__ == '__main__':
    import doctest
    doctest.testmod()

