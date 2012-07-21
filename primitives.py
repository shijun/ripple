from functools import reduce
from operator import add, sub, mul, floordiv


def as_dict(klass):
    methods = klass.__dict__.copy()
    for name, method in methods.items():
        if not name.startswith('_') and method.__doc__ != '':
            setattr(klass, method.__doc__, method)
    return klass.__dict__


@as_dict
class primitives(object):

    def plus(tail):
        '''+'''
        return reduce(add, tail)

    def minus(tail):
        '''-'''
        return reduce(sub, tail)

    def multiply(tail):
        '''*'''
        return reduce(mul, tail)

    def divide(tail):
        '''/'''
        return reduce(floordiv, tail)

    def equal(tail):
        '''='''
        return '#t' if tail[0] == tail[1] else '#f'

    def greater_than(tail):
        '''>'''
        return '#t' if tail[0] > tail[1] else '#f'

    def less_than(tail):
        '''<'''
        return '#t' if tail[0] < tail[1] else '#f'


