
# Hierarchical configuration for Python packages

[![PyPI](https://img.shields.io/pypi/v/scopedconfig.svg?maxAge=2592000)](https://pypi.org/project/scopedconfig)
[![Python Versions](https://img.shields.io/pypi/pyversions/scopedconfig.svg)](https://pypi.org/project/scopedconfig/)
[![Build status](https://travis-ci.org/etingof/scopedconfig.svg?branch=master)](https://travis-ci.org/etingof/scopedconfig)
[![Coverage Status](https://img.shields.io/codecov/c/github/etingof/scopedconfig.svg)](https://codecov.io/github/etingof/scopedconfig)
[![GitHub license](https://img.shields.io/badge/license-BSD-blue.svg)](https://raw.githubusercontent.com/etingof/scopedconfig/master/LICENSE.rst)

The `scopedconfig` library offers a simple to use and lightweight configuration
file parser for Python packages that desire their configuration information
to be expressed in a hierarchical manner.

## How to use scopedconfig

With `scopedconfig` you turn a text file containing hierarchical configuration,
expressed in a scoped option-value form, into an object through which you can
look up values by option names.

The configuration file is composed of a set of `option: value` pairs optionally
enclosed into potentially nested `block {}` constructs. Blocks provide lexical
scopes for options (so you can have same-named options in different scopes)
and a way to override the value defined in the outer scope by the value in the
inner scope.

Options are distinguished from values by trailing colon (:). There may be
several whitespace-separated values assigned to option. Values with spaces
can be quoted.

Much like directory names on the file system, block names form a path
to the nested scopes to look up options at starting from the innermost.

For example:

```bash
test-option: global-default-value

outermost-block
{
    test-option: a-bit-more-specific-value

    more-specific-block
    {
        test-option: specific-value

        very-concrete-settings
        {
            test-option: highly-specific-value
        }
    }
}
```

Evaluating the above configuration for *test-option* would yield:

```python
get_option('test-option', '') # -> global-default-value
get_option('test-option', 'outermost-block') # -> a-bit-more-specific-value
get_option('test-option', 'outermost-block',
           'more-specific-block') # -> specific-value
get_option('test-option', 'outermost-block', 'more-specific-block',
           'very-concrete-settings')  # -> highly-specific-value
```

Options specified inside a block apply to their current scopes as
well as to all nested scopes unless the same option exists there:

```bash
$ cat config.txt
outermost-block
{
    test-option: test-value

    more-specific-block
    {
        unrelated-option: value
    }
}
```

Looking up *test-option* at the above configuration would yield:

```python
get_option('test-option', '') # -> ScopedConfigError raised
get_option('test-option', 'outermost-block') # -> test-value
get_option('test-option', 'outermost-block',
           'more-specific-block') # -> test-value
```

In Python code, using the above configuration file in an application
would look like this:

```python
from scopedconfig import *

with open('config.txt') as iterable:
    cfg = ScopedConfig.load(iterable)

scopes = cfg.get_scopes('test-option')
value = cfg.get_option('test-option', *scopes)
print('Option at scope %s has value %s' % ('.'.join(scopes), value))
```

In the application, the intended configuration design is to have most
general options defined somewhere within the outer scope, more specific
values can be defined in the inner scope(s). Application then can look up
the option always at the innermost scope catching more specific values for
any given option (if it's present), and falling back to a less specific
value at the first outward scope where the desired option is present.

## How to get scopedconfig

The scopedconfig package is distributed under terms and conditions of 2-clause
BSD [license](https://github.com/etingof/scopedconfig/LICENSE.rst). Source code is freely
available as a GitHub [repo](https://github.com/etingof/scopedconfig).

You could `pip install scopedconfig` or download it from [PyPI](https://pypi.org/project/scopedconfig).

If something does not work as expected, 
[open an issue](https://github.com/etingof/scopedconfig/issues) at GitHub.

Copyright (c) 2019, [Ilya Etingof](mailto:etingof@gmail.com). All rights reserved.
