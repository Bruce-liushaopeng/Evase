import ast
import os
from typing import Dict

from backend.depanalyze.analysisutil import get_dependency_relations, dir_to_module_structure
from backend.depanalyze.modulestructure import ModuleAnalysisStruct
from backend.depanalyze.scoperesolver import ScopeResolver


class ProjectAnalysisStruct:

    def __init__(self, prj_name: str, prj_root: str):
        """
        Constructor for instances of project analysis structure.

        :param prj_name: The name of the project
        :param prj_root: The root directory of the project
        """
        self.prj_name = prj_name

        if not os.path.exists(prj_root):
            raise ValueError("Can't accept a file path that doesn't exist.")

        self._prj_root = prj_root
        self._module_structure = dir_to_module_structure(self._prj_root)
        self.resolve_scopes(ScopeResolver())
        get_dependency_relations(self._prj_root, self._module_structure)

    def resolve_module_funcs(self):
        for mdl in self._module_structure.values():
            mdl.resolve_funcs()

    def resolve_scopes(self, scr: ScopeResolver):
        for mdl in self._module_structure.values():
            mdl.resolve_scopes(scr)
            scr.reset()

    def get_prj_root(self):
        """
        Retrieve the root given for the project.

        :return: The root of the project
        """
        return self._prj_root

    def get_module_structure(self) -> Dict[str, ModuleAnalysisStruct]:
        """
        Retrieve the structure of the modules (use after processing)

        :return: Mapping of module names to analysis structures
        """
        return self._module_structure

    def get_module(self, module_key) -> ModuleAnalysisStruct:
        """
        Retrieve the structure of the module

        :return: module analysis structures
        """
        return self._module_structure.get(module_key)


if __name__ == '__main__':
    test = ProjectAnalysisStruct("parser", "C:/Users/Anthony/Desktop/Desktop/Proj/parser")

    for x in test.get_module_structure().keys():
        print("=======")
        print("key " + x)
        print(test.get_module(x).get_local_imports())
        print(test.get_module(x).get_module_imports())
        print(test.get_module(x).get_funcs())
        print(ast.dump(test.get_module(x).get_ast(), indent = 2))