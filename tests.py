import unittest

from lis import (
    tokenize, parse, close_bracket_index, run)


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


class EvalTests(unittest.TestCase):

    def test_simple_add(self):
        self.assertEqual(run(['+', 1, 2]), 3)

    def test_nested_add(self):
        self.assertEqual(run(['+', ['+', 1, ['+', 0, 2]], 3]), 6)

    def test_subtract_operation(self):
        self.assertEqual(run(['-', 3, 2]), 1)

    def test_multiple_operations(self):
        self.assertEqual(run(['-', ['+', 3, 10], ['/', ['*', 4, 5], 5]]), 9)

    def test_gt_lt_comparison(self):
        prog = ['=', ['<', 4, 3], ['>', 3, 2]]
        self.assertEqual(run(prog), False)

    def test_gte_lte_comparison(self):
        prog = ['=', ['<=', 4, 4], ['>=', 3, 2]]
        self.assertEqual(run(prog), True)

    def test_abs(self):
        self.assertEqual(run(['abs', -3]), 3)

    def test_begin(self):
        self.assertEqual(run(['begin', ['+', 1, 2], ['+', 2, 3]]), 5)


if __name__ == '__main__':
    unittest.main()
