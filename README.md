Ripple is currently an incomplete Scheme interpreter coded in Python 3. It will
have eventually have the ability to compile into native machine code and will
fully support the R7RS standard. Scheme unit tests will be used to confirm
compatibility with the standard.

Status
======

Mathematical things like factorials can be calculated with Ripple. This is
not meant to be a practical program that other people can use. I'm coding
this just for fun, and maybe hopefully I can learn a thing or two. If you
would like to use something practical that you can do awesome stuff with,
check out Racket (http://racket-lang.org/) or Python
(http://www.python.org/). =)

But what can this thing do anyway? It has support for arithmetic,
variables, if statements, and functions. Functions are first-class and
closures. Loops can be done through recursion.

Ripple hardly has any error checking, but this keeps the code nice and
simple. Most definitely a syntax error or type mismatch in any Scheme code
given to Ripple will result in a Python exception being raised. I'm
planning on adding error checking later.

Optimization of the interpreter is not a primary goal of this project. The
performance of the generated machine code is at the mercy of LLVM.

It'd be nice to have an HTML5 interface to Ripple.

Development Environment Information
===================================

I'm developing Ripple on Linux Mint 14, which is based off of Ubuntu 12.10
(Quantal Quetzal), so that means I'm using somewhat old versions of the
following: Python (3.2), PLY (3.4), and LLVM (3.1). Ripple may not work with
Python 2.

Naming
======

The name for this interpreter is Ripple, which is my particular
pronunciation for the famous Lisp acronym REPL (read-eval-print loop).
Ironically, Ripple does not currently support REPL. ;)

(Also the sea of parentheses common in Scheme and many other forms of Lisp
looks like ripples of water to me (somewhat). :) )

Licensing
=========

Ripple is licensed under GNU LGPLv3.

