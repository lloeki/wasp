from __future__ import print_function, division

import wasp.parser as parser
from wasp.ast import List, Atom, Lambda, Symbol, Nil, Truth
import wasp


py_print = print
py_eval = eval
py_list = list


class ReadError(Exception):
    pass


nil = Nil()
true = Truth()
false = Truth(False)


def atom(expr):
    return isinstance(expr, Atom)


def car(expr, context):
    return expr.car.car


def cdr(expr, context):
    return expr.car.cdr


def label(expr, context):
    symbol = expr.car
    value = expr.cdr.car
    context[symbol.name] = value
    return value


def read(string, context):
    try:
        ptree = parser.parse(string.value)
    except ValueError, e:
        raise ReadError(e.message)
    #py_print(" ^ %s" % ptree)

    try:
        ast = ptree.ast()
    except ValueError, e:
        raise ReadError(e.message)
    #py_print(" ‡ %r" % ast)

    return ast


def quote(expr, context):
    return expr


def eval(expr, context):
    if atom(expr):
        if type(expr) is Symbol:
            return context[expr.name]
        else:
            return expr

    # else it's a list
    symbol = expr.car
    args = expr.cdr

    x_args = Nil()
    if symbol.name in ['quote', 'lambda', 'cond']:
        x_args = args
    elif symbol.name in ['def']:
        for arg in reversed(py_list(args.cdr.iter())):
            x_args = List(eval(arg, context), x_args)
        x_args = List(args.car, x_args)
    else:
        for arg in reversed(py_list(args.iter())):
            x_args = List(eval(arg, context), x_args)

    expr = List(symbol, x_args)
    return apply(expr, context)


def print(string, context):
    py_print(str(string))


def apply(expr, context):
    symbol = expr.car
    args = expr.cdr
    l = eval(symbol, context)
    if type(l).__name__ == 'function':
        return l(args, context)
    else:
        symbol_names = (symbol.name for symbol in l.args.iter())
        args_dict = dict(zip(symbol_names, args.iter()))
        arg_context = wasp.Context(args_dict)
        context = context + arg_context
        return eval(l.body, context)


def lambda_(expr, context):
    args = expr.car
    body = expr.cdr.car
    return Lambda(args, body)


def list(expr, context):
    return expr


def cons(expr, context):
    return List(expr.car, expr.cdr.car)


def cond(expr, context):
    for clause in expr.iter():
        condition = eval(clause.car, context)
        if condition != false and type(condition) != Nil:
            return eval(clause.cdr.car, context)
    return Nil()


def eq(expr, context):
    if expr.car == expr.cdr.car:
        return true
    else:
        return false


def append(expr, context):
    result = Nil()
    for item in reversed(py_list(expr.cdr.car.iter())):
        result = List(item, result)
    for item in reversed(py_list(expr.car.iter())):
        result = List(item, result)
    return result


def plus(args, context):
    return args.car.value + args.cdr.car.value


def minus(args, context):
    return args.car.value - args.cdr.car.value


def multiply(args, context):
    return args.car.value * args.cdr.car.value


def div(args, context):
    return args.car.value / args.cdr.car.value
