#
# This file is part of scopedconfig software.
#
# Copyright (c) 2019, Ilya Etingof <etingof@gmail.com>
# License: https://github.com/etingof/scopedconfig/blob/master/LICENSE.rst
#
import re

SYMBOL_OPTION = ':'
SYMBOL_SECTION_BEGIN = '{'
SYMBOL_SECTION_END = '}'
SYMBOL_WORD = ''


class Lexer(object):
    def __init__(self):
        self._tokens = []
        self._index = 0

    def tokenize(self, iterable):

        self._tokens = []
        self._index = 0

        for line in iterable:

            if line.lstrip() and line.lstrip()[0] == '#':
                continue

            tokens = re.findall(r'(?:[^\s,"]|"(?:\\.|[^"])*")+', line)
            for i, tok in enumerate(tokens):
                if tok and tok.startswith('"') and tok.endswith('"'):
                    tokens[i] = tok[1:-1]

            if not tokens or not tokens[0] or tokens[0][0] == '#':
                continue

            for token in tokens:
                # Figure out the grammar type of the token
                if token and token[-1] == SYMBOL_OPTION:
                    # It's an option
                    symbol = SYMBOL_OPTION

                    # Cut the trailing char from the token
                    token = token[:-1]

                elif token == SYMBOL_SECTION_BEGIN:
                    symbol = SYMBOL_SECTION_BEGIN

                elif token == SYMBOL_SECTION_END:
                    symbol = SYMBOL_SECTION_END

                else:
                    symbol = SYMBOL_WORD

                # Attach read tokens to list of tokens
                self._tokens.append((token, symbol))

        self._index = 0

        return self

    def __iter__(self):
        if not self._tokens:
            return

        idx = -1

        while idx < len(self._tokens) - 1:
            idx += 1

            shift = (yield self._tokens[idx])

            if shift:
                idx = idx - shift
