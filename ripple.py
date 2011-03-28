#!/usr/bin/env python

import lexer
from lexer import tokens
import ply.lex as lex
lex.lex(module=lexer)

toplevel = dict()

def p_expression(p):
    '''expression : expression list
                  | terminal
                  | quote
                  | empty'''
    from evaluate import evaluate

    if len(p) == 3:
        p[0] = evaluate(p[2], toplevel)
    else:
        p[0] = evaluate(p[1], toplevel)

def p_list(p):
    '''list : '(' elements ')' '''
    p[0] = p[2]

def p_list_empty(p):
    '''list : '(' ')' '''
    p[0] = []

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

    """

    with open(program) as file:
        result = yacc.parse(file.read())
        toplevel.clear()
        return result

if __name__ == '__main__':
    from doctest import testfile
    testfile('tests/README')

