def run(program):
    """Run a valid Scheme program."""

    with open(program) as file:
        from parse import parse
        return parse(file.read())

def main(file=None):
    if file is not None:
        print(run(file))
    else:
        from doctest import testfile
        testfile('tests/README')

