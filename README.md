Ripple is currently a Scheme interpreter coded in Python. It will be made
a compiler later and will fully support the R5RS standard
(http://www.schemers.org/Documents/Standards/R5RS/). Scheme unit tests will
be used to confirm compatibility with the standard.

Naming
======

The name for this interpreter is Ripple, which is my particular
pronunciation for the famous Lisp acronym REPL (read-eval-print loop).
Ironically, Ripple does not currently support REPL. ;)

(Also the sea of parentheses common in Scheme and many other forms of Lisp
looks like ripples of water to me (somewhat). :) )

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

Optimization of the interpreter or any generated machine code is not a
primary goal of this project.

Ripple hardly has any error checking, but this keeps the code nice and
simple. Most definitely a syntax error or type mismatch in any Scheme code
given to Ripple will result in a Python exception being raised. I'm
planning on adding error checking later.

Eventually I want Ripple to generate machine code. The easiest way of
doing this is by using LLVM. I might use the Python binding for LLVM
(llvm-py), but that may prove to be limiting since it hasn't been updated
to use LLVM 2.9. Either I will fork llvm-py or have Ripple generate
LLVM assembly code directly.

Development Environment Information
===================================

I'm developing Ripple on Ubuntu 10.10 (Maverick Meerkat), so that means I'm
using somewhat old versions of the following: Python (2.6), PLY (3.3), and
LLVM (2.7). Ripple is coded with forward compatibility in mind though. It
should work in newer versions of Python at least.

Licensing
=========

Ripple is licensed under GNU LGPLv3.

