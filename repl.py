import wasp.parser as parser


class Reader(object):
    def __init__(self):
        pass

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def next(self):
        try:
            return raw_input(">> ")
        except EOFError:
            raise StopIteration()


if __name__ == "__main__":
    for line in Reader():
        ptree = parser.parse(line)
        print " ^ %s" % ptree
        ast = ptree.ast()
        print " ‡ %r" % ast
        #ast.eval()
