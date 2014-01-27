import wasp
import wasp.ast
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

    context = wasp.Context()

    for line in Reader(">> ", banner="WASP %s" % wasp.VERSION):
        if line == "" or line is None:
            continue

        try:
            ast = context['read'](wasp.ast.String(line), context)
        except wasp.lib.ReadError, e:
            print "Parse error:", e.message
            continue

        try:
            result = context['eval'](ast, context)
        except wasp.SymbolError, e:
            print "Eval error:", e.message
            continue

        try:
            context['print'](result, context)
        except Exception, e:
            print "Print error:", e.message
            continue
