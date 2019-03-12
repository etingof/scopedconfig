#
# This file is part of scopedconfig software.
#
# Copyright (c) 2019, Ilya Etingof <etingof@gmail.com>
# License: https://github.com/etingof/scopedconfig/blob/master/LICENSE.rst
#
import unittest

suite = unittest.TestLoader().loadTestsFromNames(
    ['tests.unit.__main__.suite']
)


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite)
