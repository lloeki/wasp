from unittest import TestCase
import wasp.parser as parser

class TestParser(TestCase):
    def test_atom(self):
        self.assertEqual(str(parser.parse("1")), "1")

    def test_quoted_atom(self):
        self.assertEqual(str(parser.parse("'1")), "'1")

    def test_nonalpha_symbol(self):
        self.assertEqual(str(parser.parse("+")), "+")

    def test_quoted_nonalpha_symbol(self):
        self.assertEqual(str(parser.parse("'+")), "'+")

    def test_list(self):
        self.assertEqual(str(parser.parse("(+ 1 2)")),
                         "(+ . (1 . (2 . NIL)))")

    def test_quoted_list(self):
        self.assertEqual(str(parser.parse("'(+ 1 2)")),
                         "'(+ . (1 . (2 . NIL)))")

    def test_list_in_list(self):
        self.assertEqual(str(parser.parse("(+ 1 (* 3 2))")),
                         "(+ . (1 . ((* . (3 . (2 . NIL))) . NIL)))")

    def test_lists_in_list(self):
        self.assertEqual(str(parser.parse("(+ (* 4 5) (* 3 2))")),
                         "(+ . ((* . (4 . (5 . NIL))) . ((* . (3 . (2 . NIL))) . NIL)))")

    def test_quote_in_list(self):
        self.assertEqual(str(parser.parse("(+ '1 (* 3 2))")),
                         "(+ . ('1 . ((* . (3 . (2 . NIL))) . NIL)))")

if __name__ == '__main__':
    import unittest
    unittest.main()
