#!/usr/bin/env python

import lexer
from lexer import tokens
import ply.lex as lex
lex.lex(module=lexer)

def define_variable(name, value, bindings):
    bindings[name] = evaluate(value, bindings)

def define_function(parameters, body, bindings):
    function = dict()
    function['parameters'] = parameters
    function['body'] = body
    function['closure'] = bindings.copy()
    return function

def evaluate(expression, bindings):
    if   expression is None:
        return None
    elif isinstance(expression, str): # variable
        return bindings[expression]
    elif isinstance(expression, int):
        return expression

    if expression[0] == 'lambda':
        return define_function(expression[1], expression[2:], bindings)

    if expression[0] == 'define':
        if isinstance(expression[1], list):
            function = define_function(expression[1][1:],
                                       expression[2:], bindings)
            name = expression[1][0]
            bindings[name] = function
            function['closure'][name] = function
        else:
            define_variable(expression[1], expression[2], bindings)
        return None

    if expression[0] == 'set!':
        define_variable(expression[1], expression[2], bindings)
        return None

    if expression[0] == 'if':
        predicate = expression[1]
        consequence = expression[2]
        alternative = expression[3]

        if evaluate(predicate, bindings) == '#f':
            return evaluate(alternative, bindings)
        else:
            return evaluate(consequence, bindings)

    if expression[0] == 'quote':
        tail = [str(item) for item in expression[1:]]
        return '({0})'.format(' '.join(tail))

    # Primitives and user-defined functions are below.
    # Their parameters are evaluated.
    head = expression[0]
    tail = [evaluate(item, bindings) for item in expression[1:]]

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

    # user-defined function
    function = bindings[head]
    arguments = zip(function['parameters'], tail)
    function['closure'].update(arguments)

    result = None
    for statement in function['body']:
        result = evaluate(statement, function['closure'])
    return result

toplevel = dict()

def p_expression(p):
    '''expression : expression list
                  | terminal
                  | quote
                  | empty'''

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

