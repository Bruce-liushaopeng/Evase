import unittest

from backend.depanalyze.projectstructure import ProjectAnalysisStruct
from backend.depanalyze.searching import *
from testutil import *

class TestSearching(unittest.TestCase):

    def test_find_function_call_origin(self):

        test_project = ProjectAnalysisStruct("testproject", prjroot1_filename)
        print(test_project.get_module_structure())

        runner_mdl = test_project.get_module('runner')
        used_mdl = test_project.get_module('util.helper')


        get_function_call_origin()


if __name__ == '__main__':
    unittest.main()
