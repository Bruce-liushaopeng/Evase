import unittest
import testutil

import os
from pprint import pprint

from backend.depanalyze.projectstructure import ProjectAnalysisStruct


class TestProjectAnalysisStruct(unittest.TestCase):

    def setUp(self):
        self.test_struct1 = ProjectAnalysisStruct("test1", testutil.prjroot1_filename)
        self.test_struct1.process()

    def test_project_root(self):
        self.assertEqual(testutil.prjroot1_filename, self.test_struct1.get_prj_root())

    def test_project_struct_dirs(self):


        md_struct = self.test_struct1.get_module_structure()

        total_len = 0
        for root, dirs, files in os.walk(testutil.prjroot1_filename):
            total_len += len([f for f in files if f.endswith(".py")])

        self.assertEqual(total_len, len(md_struct), "Module structure didn't have all of the .py files in it.")

    def test_other(self):
        for mdl in self.test_struct1.get_module_structure().values():
            print(mdl.get_name())
            print("MODULE LEVEL")
            print(mdl.get_module_imports())
            print("LOCAL LEVEL")
            print(mdl.get_local_imports())
