import unittest
import testutil

import os

from backend.depanalyze.projectstructure import ProjectAnalysisStruct


class TestProjectAnalysisStruct(unittest.TestCase):

    def setUp(self):
        self.test_struct1 = ProjectAnalysisStruct("test1", testutil.prjroot1_filename)

    def test_project_root(self):
        self.assertEqual(testutil.prjroot1_filename, self.test_struct1.get_prj_root())

    def test_project_struct_dirs(self):
        self.test_struct1.process()

        md_struct = self.test_struct1.get_module_structure()

        total_len = 0
        for root, dirs, files in os.walk(testutil.prjroot1_filename):
            total_len += len([f for f in files if f.endswith(".py")])

        self.assertEqual(total_len, len(md_struct), "Module structure didn't have all of the .py files in it.")
