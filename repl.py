import wasp
import wasp.parser
import readline


class Reader(object):
    def __init__(self, prompt, banner=None):
        self.prompt = prompt
        self.banner = banner

    def __iter__(self):
        if self.banner:
            print self.banner
        return self

    def next(self):
        try:
            return raw_input(self.prompt)
        except KeyboardInterrupt:
            return None
        except EOFError:
            raise StopIteration()


if __name__ == "__main__":
    readline.parse_and_bind("tab: complete")

    # TODO: autocomplete, someday
    # http://stackoverflow.com/questions/5637124
    #readline.set_completer(complete)

    for line in Reader(">> ", banner="WASP %s" % wasp.VERSION):
        if line == "" or line is None:
            continue

        try:
            ptree = wasp.parser.parse(line)
        except ValueError, e:
            print "Parse error:", e.message
            continue

        print " ^ %s" % ptree
        try:
            ast = ptree.ast()
        except ValueError, e:
            print "AST error:", e.message
            continue
        print " ‡ %r" % ast
        #ast.eval()
