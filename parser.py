from __future__ import print_function
from rply import ParserGenerator, LexerGenerator
from rply.token import BaseBox

lg = LexerGenerator()
lg.add("LPAREN", r"\(")
lg.add("RPAREN", r"\)")
lg.add("QUOTE", r"'")
lg.add("ATOM", r"[^\s()]+")
lg.ignore(r"\s+")

pg = ParserGenerator(["QUOTE", "LPAREN", "RPAREN", "ATOM"])


@pg.error
def error_handler(token):
    type = token.gettokentype()
    pos = token.getsourcepos()
    raise ValueError("unexpected %s at (%s, %s)" %
                     (type, pos.lineno, pos.colno))


@pg.production("main : sexpr")
def main(p):
    return p[0]


@pg.production("sexpr : ATOM")
@pg.production("sexpr : QUOTE sexpr")
@pg.production("sexpr : LPAREN list RPAREN")
def sexpr(p):
    if p[0].gettokentype() == "ATOM":
        return BoxAtom(p[0].getstr())
    elif p[0].gettokentype() == "QUOTE":
        return BoxQuote(p[1])
    else:
        return p[1]


@pg.production("list : sexpr")
@pg.production("list : sexpr list")
def list(p):
    if len(p) == 1:
        return BoxPair(p[0])
    else:
        return BoxPair(p[0], p[1])

lexer = lg.build()
parser = pg.build()


class BoxQuote(BaseBox):
    def __init__(self, sexpr):
        self.sexpr = sexpr

    def sexpr(self):
        return self.sexpr

    def __str__(self):
        return "' %s" % self.sexpr


class BoxPair(BaseBox):
    def __init__(self, x, y=None):
        self.x = x
        self.y = y

    def __str__(self):
        if self.y is None:
            y = "NIL"
        else:
            y = self.y
        return "(%s . %s)" % (self.x, y)


class BoxAtom(BaseBox):
    def __init__(self, atom):
        self.atom = atom

    def atom(self):
        return self.atom

    def __str__(self):
        return "%s" % (self.atom)


print(parser.parse(lexer.lex("1")))
print(parser.parse(lexer.lex("'1")))
print(parser.parse(lexer.lex("+")))
print(parser.parse(lexer.lex("'+")))
print(parser.parse(lexer.lex("(+ 1 2)")))
print(parser.parse(lexer.lex("'(+ 1 2)")))
print(parser.parse(lexer.lex("(+ 1 (* 3 2))")))
print(parser.parse(lexer.lex("'(+ 1 (* 3 2))")))
print(parser.parse(lexer.lex("(+ (* 4 5) (* 3 2))")))
print(parser.parse(lexer.lex("(+ '(* 4 5) (* 3 2))")))
