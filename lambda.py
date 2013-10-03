from lysssp import _eval, globs

print _eval(["apply", ["quote", ["lambda", [], 10]], ["quote", [20]]], globs)
