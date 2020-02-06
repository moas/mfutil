import unittest

import simpleeval

from mfutil import eval


class TestBasic(unittest.TestCase):

    def setUp(self):
        self.s = eval

    def t(self, expr, variables, should_be):
        return self.assertEqual(self.s(expr, variables), should_be)

    def test_endswith(self):
        self.t("x.endswith('foo')", {"x": "/to/foo"}, True)

    def test_split(self):
        self.t("x.split('/')[-1] == 'foo'", {"x": "/to/foo"}, True)

    def test_instance(self):
        class Foo:
            def fullpath(self):
                return "/to/foo"

        x = Foo()
        self.t("'foo' in x.fullpath()", {'x': x}, True)

    def test_re_match(self):
        self.t("bool(re_match('f[o]{2}', 'foo'))", None, True)
        self.t("bool(re_match('f[o]{2}', 'fox'))", None, False)

    def test_re_imatch(self):
        self.t("bool(re_imatch('f[o]{2}', 'Foo'))", None, True)
        self.t("bool(re_imatch('f[o]{2}', 'fox'))", None, False)

    def test_fnmatch(self):
        self.t("fnmatch_fnmatch('foo.txt', '*.txt')", None, True)

    def test_unsupported_function(self):
        with self.assertRaises(simpleeval.FunctionNotDefined):
            self.t("filter(None, (True, False))", None, (True,))
