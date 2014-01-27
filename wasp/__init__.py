from __future__ import print_function

from copy import copy
import wasp.lib as lib


VERSION = '0.0.1'


class SymbolError(Exception):
    pass


class Context(object):
    symbols = {
        'nil': lib.nil,
        'true': lib.true,
        'false': lib.false,
        'read': lib.read,
        'eval': lib.eval,
        'print': lib.print,
        'apply': lib.apply,
        'quote': lib.quote,
        'car': lib.car,
        'cdr': lib.cdr,
        'list': lib.list,
        'cons': lib.cons,
        'cond': lib.cond,
        'eq': lib.eq,
        'append': lib.append,
        'def': lib.label,
        'lambda': lib.lambda_,
        '+': lib.plus,
        '-': lib.minus,
        '*': lib.multiply,
        '/': lib.div,
    }

    def __init__(self, symbols={}):
        self.symbols = dict(self.symbols.items() + symbols.items())

    def __getitem__(self, symbol):
        try:
            return self.symbols[symbol]
        except KeyError:
            raise SymbolError(symbol)

    def __setitem__(self, symbol, value):
        self.symbols[symbol] = value

    def __add__(self, context):
        return Context(dict(self.symbols.items() + context.symbols.items()))

    def copy(self):
        return self.__class__(copy(self.symbols))
