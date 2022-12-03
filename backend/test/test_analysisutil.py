import ast

import testutil
from backend.depanalyze.projectstructure import ProjectAnalysisStruct
from backend.depanalyze.scoperesolver import ScopeResolver
from backend.depanalyze.searching import get_function_call_origin
import os

def test():
    test_struct1 = ProjectAnalysisStruct("test1", testutil.prjroot1_filename)
    scr = ScopeResolver()
    test_struct1.process()
    test_struct1.resolve_scopes(scr)
    test_struct1.resolve_module_funcs()

    print(test_struct1.get_module_structure())
    mdl = test_struct1.get_module(os.path.join(testutil.prjroot1_filename, 'runner'))

    for func in mdl.get_funcs():
        print(func.name)
        for node in ast.walk(func):
            if isinstance(node, ast.Call):
                print(get_function_call_origin(node, mdl))





if __name__ == '__main__':
    test()