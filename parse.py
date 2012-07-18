import lexer
from lexer import tokens
import ply.lex as lex
lex.lex(module=lexer)

def p_expression(p):
    '''expression : expression list
                  | terminal
                  | quote
                  | empty'''
    from evaluate import evaluate

    if len(p) == 3:
        p[0] = evaluate(p[2], p.parser.toplevel)
    else:
        p[0] = evaluate(p[1], p.parser.toplevel)

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
    else:
        p[0] = []

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
    print('Syntax error: {}'.format(p.value))

def parse(source):
    import ply.yacc as yacc
    parser = yacc.yacc()
    parser.toplevel = dict()
    return parser.parse(source)

