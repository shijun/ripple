#!/usr/bin/env python

def parse(program):
    """Parse a valid Scheme program.

    """

    with open(program) as file:
        from parse import parse
        return parse(file.read())

if __name__ == '__main__':
    from doctest import testfile
    testfile('tests/README')

