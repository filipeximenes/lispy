import unittest

from lis import tokenize, parse, close_bracket_index


class TokenizeTestCase(unittest.TestCase):

    def test_empty_brackets(self):
        self.assertEqual(tokenize('()'), ['(', ')'])

    def test_begin_statement(self):
        self.assertEqual(tokenize('(begin ())'), ['(', 'begin', '(', ')', ')'])


class CloseBracketIndexTestCase(unittest.TestCase):

    def test_single_pair(self):
        exp = ['(', ')']
        self.assertEqual(close_bracket_index(exp), 1)

    def test_token_inside(self):
        exp = ['(', 'begin', ')']
        self.assertEqual(close_bracket_index(exp), 2)

    def test_nested(self):
        exp = ['(', '(', ')', ')']
        self.assertEqual(close_bracket_index(exp), 3)

    def test_wit_other_tokens(self):
        exp = ['(', 'begin', '(', ')', ')']
        self.assertEqual(close_bracket_index(exp), 4)


class RecursiveParseTestCase(unittest.TestCase):

    def test_simple_exp(self):
        self.assertEqual(parse('(begin (+ 1 2))'), ['begin', ['+', 1, 2]])

    def test_nested_exp(self):
        self.assertEqual(parse('(begin (+ 1 (- 3 2)))'), ['begin', ['+', 1, ['-', 3, 2]]])

    def test_even_more_nested_exp(self):
        self.assertEqual(
            parse('(begin (+ (+ 3 6) (- 3 2)))'),
            ['begin', ['+', ['+', 3, 6], ['-', 3, 2]]])

    def test_even_more_more_nested_exp(self):
        self.assertEqual(
            parse('(begin (+ (+ 3 6) (- 3 2) (+ (- 1 1) 3)))'),
            ['begin', ['+', ['+', 3, 6], ['-', 3, 2], ['+', ['-', 1, 1], 3]]])

    def test_define_exp(self):
        self.assertEqual(
            parse('(begin (define r 3) (+ r 5))'),
            ['begin', ['define', 'r', 3], ['+', 'r', 5]])


if __name__ == '__main__':
    unittest.main()
