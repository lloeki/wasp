#!/usr/bin/env python

import inspect
import re

globs = {}

def isprim(name):
    return inspect.isfunction(globs.get(name, None))

def islazy(name):
    if isprim(name): return name in ['cond', 'quote', 'setq']
    return globs.get(name, [None])[0] == 'macro'

def isatom(name):
    return not (type(name) == list or type(name) == dict)

def setq(sexpr, context):
    globs[sexpr[0]] = sexpr[1]
    return sexpr[1]

def _apply(fn, args, context):
    if isprim(fn): return globs[fn](args, context)
    context = dict(zip(globs[fn][1], args))
    return _eval(globs[fn][2], context)

def _eval(sexpr, context):
    if isatom(sexpr):
        if sexpr in context:
            return context[sexpr]
        return sexpr

    fn = sexpr[0]
    args = sexpr[1:]

    if not islazy(fn):
        args = map(lambda n: _eval(n, context), args)
    return _apply(fn, args, context)

def _cond(sexpr, context):
    for elem in sexpr[0]:
        if _eval(elem[0], context): return _eval(elem[1], context)
    return False

def _read(sexpr):
    grammar = r"(\()|(\))|([^()\s]+)|(\s+)"

    def sequenceBuilder(match):
        leftbracket, rightbracket, atom, whitespace = match.groups()
        if(leftbracket): return '['
        elif(rightbracket): return ']'
        elif(atom): return '"' + atom + '"'
        elif(whitespace): return ','
    return eval(re.sub(grammar, sequenceBuilder, sexpr), None, None)

globs['setq'] = setq
globs['cond'] = _cond
globs['car'] = lambda sexpr, context: sexpr[0][0]
globs['cdr'] = lambda sexpr, context: sexpr[0][1:]
globs['quote'] = lambda sexpr, context: sexpr[0]
globs["apply"] = lambda sexpr, context: _apply(sexpr[0], sexpr[1], context)
globs['+'] = lambda sexpr, context: sexpr[0] + sexpr[1]
globs['-'] = lambda sexpr, context: sexpr[0] - sexpr[1]
globs['*'] = lambda sexpr, context: sexpr[0] * sexpr[1]
globs['/'] = lambda sexpr, context: sexpr[0] / sexpr[1]
globs['equal?'] = lambda sexpr, context: sexpr[0] == sexpr[1]

# FIXME: apply, eval the first arg
# TODO: define lambda func
# FIXME: sexpr=>lstruct
# TODO: _read, sexpr=>lstruct
# TODO: REPL while 1: print _eval(_read())

