import unittest
import ast
from api.utils import Module


class TestUtilsModule(unittest.TestCase):

    def test_module_dependencies_inline(self):
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

    def test_module_dependencies_resource(self):
        with open("resources/testmodule1.py", "r") as f:
            testmodl1 = Module("testmodule1", ast.parse(f.read()))
        with open("resources/testmodule2.py", "r") as f:
            testmodl2 = Module("testmodule2", ast.parse(f.read()))

        dep1 = testmodl1.get_dependencies()
        dep2 = testmodl2.get_dependencies()

        self.assertEqual(len(dep1), 1)
        self.assertEqual(dep1['testmodule2']['as'], 'tm2')
        fnname, fnasname = dep1['testmodule2']['funcs'][0]
        self.assertEqual(fnname, "add")
        self.assertEqual(fnasname, "plus")
        self.assertEqual(len(dep2), 0)

    def test_module_functions_resource(self):
        with open("resources/testmodule1.py", "r") as f:
            testmodl1 = Module("testmodule1", ast.parse(f.read()))
        with open("resources/testmodule2.py", "r") as f:
            testmodl2 = Module("testmodule2", ast.parse(f.read()))

        fn1 = testmodl1.get_functions()
        fn2 = testmodl2.get_functions()

        self.assertEqual(len(fn1), 4)
        self.assertIn("__init__", fn1)
        self.assertIn("perform_comp", fn1)
        self.assertIn("get_name", fn1)
        self.assertIn("main", fn1)

        self.assertEqual(len(fn2), 2)  # ensure second test module only has 2 functions in it
        self.assertIn("add", fn2)  # ensure correct function names
        self.assertIn("sub", fn2)  # ensure correct function names


if __name__ == '__main__':
    unittest.main()
