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
        predicate, consequence, alternative = expression[1:4]

        if evaluate(predicate, bindings) == '#f':
            return evaluate(alternative, bindings)
        else:
            return evaluate(consequence, bindings)

    if expression[0] == 'quote':
        tail = [str(item) for item in expression[1:]]
        return '({})'.format(' '.join(tail))

    # Primitives and user-defined functions are below.
    # Their parameters are evaluated.
    head = expression[0]
    tail = [evaluate(item, bindings) for item in expression[1:]]

    # primitives
    from functools import reduce
    from operator import add, sub, mul, floordiv

    if   head == '+':
        return reduce(add, tail)
    elif head == '-':
        return reduce(sub, tail)
    elif head == '*':
        return reduce(mul, tail)
    elif head == '/':
        return reduce(floordiv, tail)
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

    return reduce(lambda _, statement: evaluate(statement, function['closure']),
                  function['body'], None)

