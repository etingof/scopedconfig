#
# This file is part of scopedconfig software.
#
# Copyright (c) 2018-2019, Ilya Etingof <etingof@gmail.com>
# License: https://github.com/etingof/scopedconfig/blob/master/LICENSE.rst
#
import sys
import unittest

from scopedconfig.config import ScopedConfig
from scopedconfig.error import ScopedConfigError


class ScopedConfigTestCase(unittest.TestCase):

    def test_get_paths_to_attr_ok(self):
        text = """\
# comment
a: b
x {
    a: b

    # comment
    y {
        a: "b c"

        z {
            b: a
        }
    }
}
"""
        cfg = ScopedConfig().load(text.split('\n'))

        result = cfg.get_scopes('a')

        expected = [
            ('',), ('', 'x'), ('', 'x', 'y')
        ]

        self.assertEqual(expected, result)

    def test_get_paths_to_attr_missing(self):
        text = """\
x {
    y {
      a: "b"
    }
}
"""
        cfg = ScopedConfig().load(text.split('\n'))

        result = cfg.get_scopes('b')

        expected = []

        self.assertEqual(expected, result)

    def test_get_option_ok(self):
        text = """\
a: b
x {
    a: b

    y {
        a: "b b"

        z {
            b: a
        }
    }
}
"""
        cfg = ScopedConfig().load(text.split('\n'))

        result = cfg.get_option('a', '', 'x', 'y')

        expected = 'b b'

        self.assertEqual(expected, result)

    def test_get_option_shorter_path(self):
        text = """\
a: b
x {
    a: b

    y {
        a: "b b"

        z {
            b: a
        }
    }
}
"""
        cfg = ScopedConfig().load(text.split('\n'))

        result = cfg.get_option('a', '', 'x')

        expected = 'b'

        self.assertEqual(expected, result)

    def test_get_option_ok_vector(self):
        text = """\
a: b
x {
    a: b

    y {
        a: b c

        z {
            b: a
        }
    }
}
"""
        cfg = ScopedConfig().load(text.split('\n'))

        result = cfg.get_option('a', '', 'x', 'y', vector=True)

        expected = ['b', 'c']

        self.assertEqual(expected, result)

    def test_get_option_ok_default(self):
        text = """\
a: b
x {
    a: b

    y {
        a: b c

        z {
            b: a
        }
    }
}
"""
        cfg = ScopedConfig().load(text.split('\n'))

        result = cfg.get_option('q', '', 'x', 'y', default='z')

        expected = 'z'

        self.assertEqual(expected, result)

    def test_get_option_ok_missing(self):
        text = """\
a: b
x {
    a: b

    y {
        a: b c

        z {
            b: a
        }
    }
}
"""
        cfg = ScopedConfig().load(text.split('\n'))

        self.assertRaises(
            ScopedConfigError, cfg.get_option, 'q', '', 'x', 'y')


suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite)
