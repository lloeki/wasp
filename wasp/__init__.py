from __future__ import print_function


import wasp.lib as lib


VERSION = '0.0.1'


class SymbolError(Exception):
    pass


class Context(object):
    symbols = {
        '+': lib.plus,
        '-': lib.minus,
        '*': lib.multiply,
        '/': lib.div,
        'read': lib.read,
        'eval': lib.eval,
        'print': lib.print,
        'apply': lib.apply,
        'quote': lib.quote,
    }

    def __getitem__(self, symbol):
        try:
            return self.symbols[symbol]
        except KeyError:
            raise SymbolError(symbol)
