import unittest
import ast
from utils import Module

class TestUtilsModule(unittest.TestCase):

    def test_module_dependencies(self):
        # case 1, from import with as on function
        testmodl = Module("random path", ast.parse("from alpha import beta as charlie"))
        dep = testmodl.dependencies
        self.assertTrue("alpha" in dep)
        self.assertIsNone(dep['alpha']['as'])
        self.assertEqual(len(dep['alpha']['funcs']), 1)
        imprtname, imprtasname = dep['alpha']['funcs'][0]
        self.assertEqual(imprtname, "beta")
        self.assertEqual(imprtasname, "charlie")

        # case 2, import from __init__.py
        testmodl = Module("random path", ast.parse("from . import module as modl, module2"))
        dep = testmodl.dependencies
        self.assertTrue(None in dep)
        self.assertIsNone(dep[None]['as'])
        self.assertEqual(len(dep[None]['funcs']), 2)
        imprtname, imprtasname = dep[None]['funcs'][0]
        self.assertEqual(imprtname, "module")
        self.assertEqual(imprtasname, "modl")
        imprtname, imprtasname = dep[None]['funcs'][1]
        self.assertEqual(imprtname, "module2")
        self.assertEqual(imprtasname, None)

        # case 3, import with as
        testmodl = Module("random path", ast.parse("import utils as u"))
        dep = testmodl.dependencies
        self.assertTrue("utils" in dep)
        self.assertEqual(dep['utils']['as'], "u")
        self.assertEqual(len(dep['utils']['funcs']), 0)

if __name__ == '__main__':
    unittest.main()