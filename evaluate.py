def define_variable(name, value, bindings):
    bindings[name] = evaluate(value, bindings)

def define_function(parameters, body, bindings):
    return {
        'parameters': parameters,
        'body': body,
        'closure': bindings.copy(),
    }

def evaluate(expression, bindings):
    if isinstance(expression, list):
        head = expression[0]
        tail = expression[1:]
    elif isinstance(expression, str):
        return bindings[expression]
    elif isinstance(expression, int):
        return expression
    else:
        return

    if head == 'lambda':
        return define_function(tail[0], tail[1:], bindings)

    if head == 'define':
        if isinstance(tail[0], list):
            function = define_function(tail[0][1:], tail[1:], bindings)
            name = tail[0][0]
            bindings[name] = function
            function['closure'][name] = function
        else:
            define_variable(tail[0], tail[1], bindings)
        return

    if head == 'set!':
        define_variable(tail[0], tail[1], bindings)
        return

    if head == 'if':
        predicate, consequence, alternative = tail[:3]

        if evaluate(predicate, bindings) == '#f':
            return evaluate(alternative, bindings)
        else:
            return evaluate(consequence, bindings)

    if head == 'quote':
        tail = [str(item) for item in tail]
        return '({})'.format(' '.join(tail))

    # Primitives and user-defined functions are below.
    # Their parameters are evaluated.
    tail = [evaluate(item, bindings) for item in tail]

    from primitives import primitives
    try:
        return primitives[head](tail)
    except KeyError:
        pass

    # user-defined function
    function = bindings[head]
    arguments = zip(function['parameters'], tail)
    function['closure'].update(arguments)

    from functools import reduce
    return reduce(lambda _, statement: evaluate(statement, function['closure']),
                  function['body'], None)

