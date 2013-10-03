from __future__ import print_function
from pprint import pprint
from rply import ParserGenerator, LexerGenerator
from rply.token import BaseBox

lg = LexerGenerator()
lg.add("LPAREN", r"\(")
lg.add("RPAREN", r"\)")
lg.add("ATOM", r"[^\s()]+")
lg.ignore(r"\s+")

pg = ParserGenerator(["LPAREN", "RPAREN", "ATOM"])


@pg.error
def error_handler(token):
    raise ValueError("unexpected %s" % token.gettokentype())


@pg.production("main : sexpr")
def main(p):
    return p[0]


@pg.production("sexpr : LPAREN expr RPAREN")
def sexpr(p):
    return BoxSexpr(p[1])


@pg.production("expr : ATOM")
def atom(p):
    return BoxAtom(p[0].getstr())


@pg.production("expr : ATOM sexpr")
@pg.production("expr : ATOM expr")
def sexpr(p):
    return BoxExpr(BoxAtom(p[0].getstr()), p[1])

lexer = lg.build()
parser = pg.build()


class BoxSexpr(BaseBox):
    def __init__(self, expr):
        self.expr = expr

    def expr(self):
        return self.expr

    def __str__(self):
        return "( %s )" % (self.expr)


class BoxExpr(BaseBox):
    def __init__(self, atom, expr):
        self.atom = atom
        self.expr = expr

    def atom(self):
        return self.atom

    def expr(self):
        return self.expr

    def __str__(self):
        return "%s . ( %s )" % (self.atom, self.expr)


class BoxAtom(BaseBox):
    def __init__(self, atom):
        self.atom = atom

    def atom(self):
        return self.atom

    def __str__(self):
        return "%s" % (self.atom)

print(parser.parse(lexer.lex("(+ 1 (* 3 2))")))
