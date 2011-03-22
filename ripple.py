#!/usr/bin/env python

from ply.lex import TOKEN

tokens = [
    'STRING',
    'ATOM',
    'BOOL',
    'NUMBER',
    'CODE',
]

reserved = {
   'define': 'DEFINE',
}

tokens += reserved.values()

# An atom is a letter or symbol, followed by
# any number of letters, digits, or symbols.
symbol = r'[!$%&|*+-/:<=>?@^_~]'
identifier = r'([A-Za-z]|%s)' % symbol + r'(\w|%s)*' % symbol
@TOKEN(identifier)
def t_ATOM(t):
    t.type = reserved.get(t.value, 'ATOM') # check for reserved words
    return t

t_STRING = r'"(\\[abtnvfr"\\\W]|[^\\"])*"'

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

# --- quoting lexer code is below ---

states = (
    ('code', 'exclusive'),
)

def t_code(t):
    r"'\("
    t.lexer.start = t.lexer.lexpos - 1
    t.lexer.level = 1
    t.lexer.push_state('code')

def t_code_left(t):     
    r'\('
    t.lexer.level += 1

def t_code_right(t):
    r'\)'
    t.lexer.level -= 1

    if t.lexer.level == 0:
         t.value = t.lexer.lexdata[t.lexer.start:t.lexer.lexpos]
         t.type = 'CODE'
         t.lexer.pop_state()
         return t

t_code_ignore = ''

def t_code_error(t):
    t.lexer.skip(1)

# --- quoting lexer code ends ---

import ply.lex as lex
lexer = lex.lex()

variables = {}

def p_expression(p):
    '''expression : expression list
                  | list
                  | CODE
                  | terminal'''
    if len(p) == 3:
        p[0] = p[2]
    else:
        p[0] = p[1]

def p_list_define(p):
    '''list : '(' DEFINE ATOM terminal ')' '''
    name = p[3]
    variables[name] = p[4]
    p[0] = p[4]

def p_list_arithmetic(p):
    '''list : '(' ATOM operands ')' '''
    from operator import add, sub, mul, div
    from functools import reduce

    if   p[2] == '+':
        p[0] = reduce(add, p[3])
    elif p[2] == '-':
        p[0] = reduce(sub, p[3])
    elif p[2] == '*':
        p[0] = reduce(mul, p[3])
    elif p[2] == '/':
        p[0] = reduce(div, p[3])

def p_operands(p):
    '''operands : operands terminal
                | operands list
                | empty'''
    # the following is a left unfold [i.e. opposite of foldl()]
    if len(p) == 3:
        if p[1] is None: # at the beginning of the list
            p[1] = []
        p[0] = p[1] + [p[2]]

def p_terminal(p):
    '''terminal : BOOL
                | STRING
                | NUMBER'''
    p[0] = p[1]

def p_terminal_atom(p):
    '''terminal : ATOM'''
    p[0] = variables[p[1]]

def p_empty(p):
    '''empty :'''
    pass

def p_error(p):
    print('Syntax error: %s' % p.value)

import ply.yacc as yacc
yacc.yacc()

def parse(program):
    """Parse a valid Scheme program.

    >>> parse('simple.scm')
    4

    >>> parse('many-terms.scm')
    372

    >>> parse('variable.scm')
    10

    >>> parse('quote.scm')
    '(3 2 1)'
    """

    with open(program) as file:
        return yacc.parse(file.read())

if __name__ == '__main__':
    import doctest
    doctest.testmod()

