class Node(object):
    pass


class List(Node):
    def __init__(self, car, cdr=None):
        self.car = car
        self.cdr = cdr

    def eval(self):
        pass

    def __repr__(self):
        return "<List %r %r>" % (self.car, self.cdr)


class Atom(Node):
    pass


class Operator(Node):
    pass


class Number(Atom):
    def __init__(self, value):
        self.value = value

    def eval(self):
        return self.value

    def __repr__(self):
        return "<Number %s>" % self.value


class Symbol(Atom):
    pass


class Quote(Node):
    def __init__(self, sexpr):
        self.sexpr = sexpr

    def eval(self):
        return self.sexpr.eval()

    def __repr__(self):
        return "<Quote %r>" % self.sexpr


class Lambda(Node):
    pass
