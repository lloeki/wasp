class Node(object):
    pass


class List(Node):
    def __init__(self, car, cdr=None):
        self.car = car
        self.cdr = cdr

    def eval(self, context):
        return context['apply'](self.car, self.cdr, context)

    def __repr__(self):
        return "<List %r %r>" % (self.car, self.cdr)


class Atom(Node):
    pass


class Operator(Node):
    pass


class Number(Atom):
    def __init__(self, value):
        self.value = value

    def eval(self, context):
        return self.value

    def __repr__(self):
        return "<%s %s>" % (type(self).__name__, self.value)


class Integer(Number):
    pass


class Float(Number):
    pass


class Symbol(Atom):
    def __init__(self, value):
        self.value = value

    def eval(self, context):
        return context[self.value]

    def __repr__(self):
        return "<Symbol %s>" % self.value


class String(Atom):
    def __init__(self, value):
        self.value = value

    def eval(self, context):
        return self.value

    def __repr__(self):
        return "<String %s>" % self.value


class Quote(Node):
    def __init__(self, sexpr):
        self.sexpr = sexpr

    def eval(self, context):
        return context['quote'](self.sexpr)

    def __repr__(self):
        return "<Quote %r>" % self.sexpr


class Lambda(Node):
    pass
