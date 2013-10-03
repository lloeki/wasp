from rply.token import BaseBox

class Quote(BaseBox):
    def __init__(self, sexpr):
        self.sexpr = sexpr

    def sexpr(self):
        return self.sexpr

    def __str__(self):
        return "'%s" % self.sexpr


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


class Atom(BaseBox):
    def __init__(self, atom):
        self.atom = atom

    def atom(self):
        return self.atom

    def __str__(self):
        return "%s" % (self.atom)


