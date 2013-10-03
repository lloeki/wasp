from lysssp import _eval, globs

_eval(['setq', 'factorial', ['lambda', ['x'], 
    ['cond', [
        [ ['equal?', 'x', 0], 1 ], 
        [ True, [ '*', 'x', ['factorial', ['-', 'x', 1]]]]]]]], globs)

def test():
    print _eval(['factorial', 10], globs)

import timeit

print timeit.Timer(test).timeit(1)
