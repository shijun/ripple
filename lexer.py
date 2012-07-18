tokens = [
    'ATOM',
    'STRING',
    'QUOTE',
    'BOOL',
    'NUMBER',
]

# An atom is a letter or symbol, followed by
# any number of letters, digits, or symbols.
symbol = '!$%&|*+-/:<=>?@^_~'
t_ATOM = r'[A-Za-z{}]'.format(symbol) + r'[\w{}]*'.format(symbol)

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
    print('Unknown character: {}'.format(t.value[0]))
    t.lexer.skip(1)

