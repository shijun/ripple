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

t_BOOL = r'\#[tf]'

t_NUMBER = r'\d+|\#b[01]+|\#o[0-7]+|\#d\d+|\#x[\dA-Fa-f]+'

t_ignore = ' '

literals = '()'

def t_error(t):
    print('Illegal character: %s' % t.value[0])
    t.lexer.skip(1)

import ply.lex as lex
lexer = lex.lex()

def p_expression(p):
    '''expression : expression list
                  | terminal
                  | empty'''

def p_list(p):
    '''list : '(' ATOM expression ')' '''
    print('operation: %s' % p[2])
    p[0] = p[3]

def p_terminal(p):
    '''terminal : ATOM
                | BOOL
                | STRING
                | NUMBER'''
    if p[1] == '#t':
        print(True)
    elif p[1] == '#f':
        print(False)
    else:
        print('operand: %s' % p[1])

def p_empty(p):
    '''empty :'''
    pass

def p_error(p):
    print('Syntax error: %s' % p.value)

import ply.yacc as yacc
yacc.yacc()

if __name__ == '__main__':
    from sys import argv
    yacc.parse(argv[1])

