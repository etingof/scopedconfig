#
# This file is part of scopedconfig software.
#
# Copyright (c) 2018-2019, Ilya Etingof <etingof@gmail.com>
# License: https://github.com/etingof/scopedconfig/blob/master/LICENSE.rst
#
import sys
import unittest

from scopedconfig.lexer import Lexer


class LexerTestCase(unittest.TestCase):

    def setUp(self):
        self._lexer = Lexer()
        super(LexerTestCase, self).setUp()

    def test_whitespace(self):
        tokens = list(self._lexer.tokenize(['   \t\t  \t \r  \n\n']))
        self.assertFalse(tokens)

    def test_option_and_value_set(self):
        text = """\
a: b
a:  b
a: "b"
"""
        tokens = list(self._lexer.tokenize(text.split('\n')))

        expected = [
            ('a', ':'), ('b', ''), ('a', ':'), ('b', ''),
            ('a', ':'), ('b', '')]

        self.assertEqual(expected, tokens)

    def test_comments(self):
        text = """\
#
# a: v
#a:
# a b
"""
        tokens = list(self._lexer.tokenize(text.split('\n')))

        expected = []

        self.assertEqual(expected, tokens)

    def test_block_options_and_values(self):
        text = """\
{
a: b
   a: b
a: "b"
       a:   "b"
}
"""
        tokens = list(self._lexer.tokenize(text.split('\n')))

        expected = [
            ('{', '{'), ('a', ':'), ('b', ''), ('a', ':'),
            ('b', ''), ('a', ':'), ('b', ''), ('a', ':'),
            ('b', ''), ('}', '}')]

        self.assertEqual(expected, tokens)

    def test_block_comments(self):
        text = """\
{
#
# a:
# a: b
}
"""
        tokens = list(self._lexer.tokenize(text.split('\n')))

        expected = [('{', '{'), ('}', '}')]

        self.assertEqual(expected, tokens)

    def test_block_blank_lines(self):
        text = """\
{


}
"""
        tokens = list(self._lexer.tokenize(text.split('\n')))
        self.assertEqual(tokens, [('{', '{'), ('}', '}')])

    def test_configuration(self):
        text = """\
# h
a: b
{
  a: b
}
"""
        tokens = list(self._lexer.tokenize(text.split('\n')))

        expected = [
            ('a', ':'), ('b', ''), ('{', '{'), ('a', ':'),
            ('b', ''), ('}', '}')]

        self.assertEqual(expected, tokens)


suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite)
