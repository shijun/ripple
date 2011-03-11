#!/usr/bin/env python

tokens = (
    'SYMBOL',
)

t_SYMBOL = r'[!#$%&|*+-/:<=>?@^_~]'

t_ignore = ' '

def t_error(t):
    print('Illegal character: %s' % t.value[0])
    t.lexer.skip(1)

import ply.lex as lex
lexer = lex.lex()

if __name__ == '__main__':
    from sys import argv
    lexer.input(argv[1])

    for token in lexer:
        print('Found value')

