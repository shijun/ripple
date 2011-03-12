#!/usr/bin/env python

tokens = (
    'STRING',
    'ATOM',
    'BOOL',
    'NUMBER',
)

t_STRING = r'"(\\[abtnvfr"\\\W]|[^\\"])*"'

# An atom is a letter or symbol, followed by
# any number of letters, digits, or symbols.
symbol = r'[!$%&|*+-/:<=>?@^_~]'
t_ATOM = r'([A-Za-z]|%s)' % symbol + r'(\w|%s)*' % symbol

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

t_ignore = ' '

literals = '()'

def t_error(t):
    print('Illegal character: %s' % t.value[0])
    t.lexer.skip(1)

import ply.lex as lex
lexer = lex.lex()

def p_expression(p):
    '''expression : list
                  | terminal
                  | empty'''
    p[0] = p[1]

def p_list(p):
    '''list : '(' ATOM operands ')' '''
    from operator import add, sub, mul, div
    from functools import reduce

    if p[2] == '+':
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
    '''terminal : ATOM
                | BOOL
                | STRING
                | NUMBER'''
    p[0] = p[1]

def p_empty(p):
    '''empty :'''
    pass

def p_error(p):
    print('Syntax error: %s' % p.value)

import ply.yacc as yacc
yacc.yacc()

if __name__ == '__main__':
    from sys import argv
    print(yacc.parse(argv[1]))

