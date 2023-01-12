import unittest

from backend.depanalyze.analysisutil import *
from testutil import *

class TestAnalysisUtil(unittest.TestCase):

    def test_dir_to_module_structure(self):

        test_mdl_struct = dir_to_module_structure(prjroot1_filename)
        print(test_mdl_struct)


if __name__ == '__main__':
    unittest.main()