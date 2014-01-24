import wasp.parser as parser

line = raw_input(">> ")
while line != "":
    tree = parser.parse(line)
    print "^^", tree
    #tree.eval()
    line = raw_input(">> ")
