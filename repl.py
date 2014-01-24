import wasp.parser as parser

line = raw_input(">> ")
while line != "":
    ptree = parser.parse(line)
    print " ^ %s" % ptree
    ast = ptree.ast()
    print " ‡ %r" % ast
    #tree.eval()
    line = raw_input(">> ")
