from rply import ParserGenerator, LexerGenerator
import box


lg = LexerGenerator()
lg.add("LPAREN", r"\(")
lg.add("RPAREN", r"\)")
lg.add("QUOTE", r"'")
lg.add("ATOM", r"[^\s()]+")
lg.ignore(r"\s+")

pg = ParserGenerator(["QUOTE", "LPAREN", "RPAREN", "ATOM"],
                     precedence=[],
                     cache_id="wasp")


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
        return box.Atom(p[0].getstr())
    elif p[0].gettokentype() == "QUOTE":
        return box.Quote(p[1])
    else:
        return p[1]


@pg.production("list : sexpr")
@pg.production("list : sexpr list")
def list(p):
    if len(p) == 1:
        return box.Pair(p[0])
    else:
        return box.Pair(p[0], p[1])

lexer = lg.build()
parser = pg.build()

def parse(string):
    return parser.parse(lexer.lex(string))
