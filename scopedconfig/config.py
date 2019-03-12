#
# This file is part of scopedconfig software.
#
# Copyright (c) 2019, Ilya Etingof <etingof@gmail.com>
# License: https://github.com/etingof/scopedconfig/blob/master/LICENSE.rst
#

from scopedconfig import error
from scopedconfig import parser
from scopedconfig import lexer


class ScopedConfig(object):
    def __init__(self):
        self.objects = {}

    def load(self, iterable):
        self.objects = parser.ScopedParser(
            lexer.Lexer().tokenize(iterable)).parse()

        return self

    def traverse(self, objects, nodes):
        """Return the leaf object resulted by traversing config
           objects tree by nodes
        """
        for obj in objects:
            # Compare obj name with node name
            #            if '_compiled_name' not in obj:
            #                obj['_compiled_name'] = re.compile(obj['_name'])
            #            if obj['_compiled_name'].match(nodes[0]):
            if obj['_name'] == nodes[0]:
                if len(nodes) == 1:
                    return obj

                r = self.traverse(obj['_children'], nodes[1:])
                if r is None:
                    return obj

                return r

    def get_scopes(self, attr, objects=None, nodes=None, paths=None):
        if objects is None:
            objects = self.objects

        if nodes is None:
            nodes = ()

        if paths is None:
            paths = []

        nodes += objects['_name'],

        if attr in objects:
            paths.append(nodes)

        for _objs in objects['_children']:
            self.get_scopes(attr, _objs, nodes, paths)

        return paths

    def get_option(self, attr, *nodes, **kwargs):
        scope = nodes

        while scope:
            obj = self.traverse([self.objects], scope)

            if obj and attr in obj:
                expect = kwargs.get('expect')

                if 'vector' in kwargs:
                    if expect:
                        try:
                            return [expect(x) for x in obj[attr]]

                        except Exception:
                            raise error.ScopedConfigError(
                                '%s value casting error at scope "%s" attribute'
                                ' "%s"' % (self, '.'.join(nodes), attr))
                    else:
                        return obj[attr]

                else:
                    if obj[attr]:

                        if expect:

                            try:
                                return expect(obj[attr][0])

                            except Exception:
                                raise error.ScopedConfigError(
                                    '%s value casting error at scope "%s" '
                                    'attribute "%s"' % (self, '.'.join(nodes),
                                                        attr))
                        else:
                            return obj[attr][0]

                    else:
                        return ''

            scope = scope[:-1]

        if 'default' in kwargs:
            return kwargs['default']

        raise error.ScopedConfigError(
            '%s non-existing attribute "%s" at scope '
            '"%s"' % (self, attr, '.'.join(nodes)))
