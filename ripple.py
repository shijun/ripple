#!/usr/bin/env python

tokens = (
    'SYMBOL',
    'STRING',
    'ATOM',
    'NUMBER',
)

t_SYMBOL = r'[!$%&|*+-/:<=>?@^_~]'

t_STRING = r'"(\\[abtnvfr"\\\W]|[^\\"])*"'

# An atom is a letter or symbol, followed by
# any number of letters, digits, or symbols.
t_ATOM = r'([A-Za-z]|' + t_SYMBOL + r')' + \
         r'(\w*|' + t_SYMBOL + r'*)'

t_NUMBER = r'\d+|\#b[01]+|\#o[0-7]+|\#d\d+|\#x[\dA-Fa-f]+'

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

