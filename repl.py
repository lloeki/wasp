import wasp
import wasp.parser
import readline

readline.parse_and_bind("tab: complete")


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
    for line in Reader(">> ", banner="WASP %s" % wasp.VERSION):
        if line == "" or line is None:
            continue

        try:
            ptree = wasp.parser.parse(line)
        except ValueError, e:
            print e.message
            continue

        print " ^ %s" % ptree
        ast = ptree.ast()
        print " ‡ %r" % ast
        #ast.eval()
