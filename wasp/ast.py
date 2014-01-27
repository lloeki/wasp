class Node(object):
    pass


class Atom(Node):
    pass


class Nil(Atom):
    def __init__(self):
        self.car = self
        self.cdr = self

    def iter(self):
        return []

    def __str__(self):
        return "nil"

    def __repr__(self):
        return "<Nil>"


class Truth(Atom):
    def __init__(self, true=True):
        self.true = true

    def __str__(self):
        return ("%s" % self.true).lower()

    def __repr__(self):
        return "<%s>" % self.true


class List(Node):
    def __init__(self, car, cdr=Nil()):
        self.car = car
        self.cdr = cdr

    def iter(self):
        car = self.car
        cdr = self.cdr
        while not type(cdr) is Nil:
            yield car
            car = cdr.car
            cdr = cdr.cdr
        else:
            yield car

    def __str__(self):
        return "(%s)" % (' '.join(str(i) for i in self.iter()))

    def __repr__(self):
        return "<List %r %r>" % (self.car, self.cdr)


class Number(Atom):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "%s" % self.value

    def __repr__(self):
        return "<%s %s>" % (type(self).__name__, self.value)

    def __eq__(self, other):
        return self.value == other.value


class Integer(Number):
    pass


class Float(Number):
    pass


class Symbol(Atom):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "%s" % self.name

    def __repr__(self):
        return "<Symbol %s>" % self.name


class String(Atom):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return '"%s"' % self.value

    def __repr__(self):
        return "<String %s>" % self.value


class Quote(List):
    def __init__(self, sexpr):
        self.car = Symbol('quote')
        self.cdr = sexpr
        self.sexpr = self.cdr

    def __str__(self):
        return "'%s" % self.sexpr

    def __repr__(self):
        return "<Quote %r>" % self.sexpr


class Lambda(Node):
    def __init__(self, args, body):
        self.args = args
        self.body = body

    def __str__(self):
        return "lambda %s %s" % (self.args, self.body)

    def __repr__(self):
        return "<Lambda %r %r>" % (self.args, self.body)
