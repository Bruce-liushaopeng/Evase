import unittest

from backend.depanalyze.analysisutil import *
from testutil import *


class TestAnalysisUtil(unittest.TestCase):

    def test_dir_to_module_structure(self):
        """
        Test made specifically for the module structure of the test project 'prjstructtest'.
        """
        test_mdl_struct = dir_to_module_structure(prjroot1_filename)
        self.assertIn('prjstructtest.runner', test_mdl_struct)
        self.assertIn('prjstructtest.__init__', test_mdl_struct)
        self.assertIn('prjstructtest.test.__init__', test_mdl_struct)
        self.assertIn('prjstructtest.util.helper', test_mdl_struct)
        self.assertIn('prjstructtest.util.__init__', test_mdl_struct)
        self.assertIn('prjstructtest.util.moreutil.helper2', test_mdl_struct)
        self.assertIn('prjstructtest.util.moreutil.__init__', test_mdl_struct)



if __name__ == '__main__':
    unittest.main()
