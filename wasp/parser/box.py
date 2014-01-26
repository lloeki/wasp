import re
from rply.token import BaseBox
from wasp import ast


class Quote(BaseBox):
    def __init__(self, sexpr):
        self.sexpr = sexpr

    def sexpr(self):
        return self.sexpr

    def __str__(self):
        return "'%s" % self.sexpr

    def ast(self):
        return ast.Quote(self.sexpr.ast())


class Pair(BaseBox):
    def __init__(self, x, y=None):
        self.x = x
        self.y = y

    def __str__(self):
        if self.y is None:
            y = "NIL"
        else:
            y = self.y
        return "(%s . %s)" % (self.x, y)

    def _r_cdr(self, cdr):
        if self.y is None:
            return (self.x.ast(), )
        else:
            return cdr + (self.x.ast(), ) + self.y._r_cdr(cdr)

    def ast(self):
        car = self.x.ast()

        if self.y is None:
            cdr = None
        elif type(self.y) is Pair:
            cdr = list(self.y._r_cdr(()))
        else:
            cdr = self.y.ast()

        return ast.List(car, cdr)


class Atom(BaseBox):
    def __init__(self, atom):
        self.atom = atom

    def atom(self):
        return self.atom

    def __str__(self):
        return "%s" % (self.atom)

    def ast(self):
        if self.atom[0] == '"':
            if self.atom[-1] == '"':
                return ast.String(self.atom)
            else:
                raise ValueError("missing \"")
        elif re.match(r'^\d+$', self.atom):
            return ast.Integer(int(self.atom))
        elif re.match(r'^\d+\.(\d+)$', self.atom):
            return ast.Float(float(self.atom))
        else:
            return ast.Symbol(self.atom)
