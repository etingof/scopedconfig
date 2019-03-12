#
# This file is part of scopedconfig software.
#
# Copyright (c) 2018-2019, Ilya Etingof <etingof@gmail.com>
# License: https://github.com/etingof/scopedconfig/blob/master/LICENSE.rst
#
import sys
import unittest

from scopedconfig.lexer import Lexer
from scopedconfig.parser import ScopedParser


class ScopedParserTestCase(unittest.TestCase):

    def test_empty(self):
        text = """\

"""
        parser = ScopedParser(Lexer().tokenize(text.split('\n')))

        ast = parser.parse()

        expected = {
            '_name': '',
            '_children': []
        }

        self.assertEqual(expected, ast)

    def test_option_and_value_set(self):
        text = """\
a: b
a2:  b
a3: "b"
"""
        parser = ScopedParser(Lexer().tokenize(text.split('\n')))

        ast = parser.parse()

        expected = {
            '_name': '',
            '_children': [],
            'a': ['b'],
            'a2': ['b'],
            'a3': ['b']
        }

        self.assertEqual(expected, ast)

    def test_comments(self):
        text = """\
#
# a: v
#a:
# a b
"""
        parser = ScopedParser(Lexer().tokenize(text.split('\n')))

        ast = parser.parse()

        expected = {
            '_name': '',
            '_children': []
        }

        self.assertEqual(expected, ast)

    def test_block_options_and_values(self):
        text = """\
x {
a: b
   a2: b
a3: "b"
       a4:   "b"
}
"""
        parser = ScopedParser(Lexer().tokenize(text.split('\n')))

        ast = parser.parse()

        expected = {
            '_name': '',
            '_children': [
                {'_name': 'x',
                 '_children': [],
                 'a': ['b'],
                 'a2': ['b'],
                 'a3': ['b'],
                 'a4': ['b']}]
        }

        self.assertEqual(expected, ast)

    def test_block_comments(self):
        text = """\
x {
#
# a:
# a: b
}
"""
        parser = ScopedParser(Lexer().tokenize(text.split('\n')))

        ast = parser.parse()

        expected = {
            '_name': '',
            '_children': [
                {'_name': 'x',
                 '_children': []}
            ]
        }

        self.assertEqual(expected, ast)

    def test_block_blank_lines(self):
        text = """\
x {


}
"""
        parser = ScopedParser(Lexer().tokenize(text.split('\n')))

        ast = parser.parse()

        expected = {
            '_name': '',
            '_children': [
                {'_name': 'x',
                 '_children': []}
            ]
        }

        self.assertEqual(expected, ast)

    def test_configuration(self):
        text = """\
# h
a: b
x {
  a: b
}
"""
        parser = ScopedParser(Lexer().tokenize(text.split('\n')))

        ast = parser.parse()

        expected = {
            '_name': '',
            '_children': [
                {'_name': 'x',
                 '_children': [],
                 'a': ['b']}
            ],
            'a': ['b']}

        self.assertEqual(expected, ast)


suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite)
