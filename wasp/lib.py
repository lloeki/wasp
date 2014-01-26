from __future__ import print_function

import wasp.parser


py_print = print
py_eval = eval


class ReadError(Exception):
    pass


def plus(a, b):
    return a + b


def minus(a, b):
    return a - b


def multiply(a, b):
    return a * b


def div(a, b):
    return a / b


def read(string):
    try:
        ptree = wasp.parser.parse(string)
    except ValueError, e:
        raise ReadError(e.message)
    py_print(" ^ %s" % ptree)

    try:
        ast = ptree.ast()
    except ValueError, e:
        raise ReadError(e.message)
    py_print(" ‡ %r" % ast)

    return ast


def eval(ast, context):
    # eval value unless list
    # eval args unless lazy
    # eval call
    return ast.eval(context)


def apply(a, b, context):
    # move to eval
    args = [arg.eval(context) for arg in b]
    return a.eval(context)(*args)


def quote(a):
    return a


def print(string):
    py_print(string)
