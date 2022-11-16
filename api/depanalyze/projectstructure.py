from typing import Dict, List

import os
from modulestructure import ModuleAnalysisStruct
from analysisutil import get_dependency_relations, dir_to_module_structure
from pprint import pprint


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
        self._dependencies = {}  # to be kept none? may need it later
        self._module_structure = {}

    def process(self):
        self._module_structure = dir_to_module_structure(self._prj_root)
        self._dependencies = get_dependency_relations(self._prj_root)

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

    def get_dependencies(self) -> Dict[str, List[str]]:
        """
        Retreive prototypical dependencies.

        :return: A mapping of
        """
        return self._dependencies


if __name__ == '__main__':
    test = ProjectAnalysisStruct("EvaseTest", "C:/courses/SYSC_4907/Evase/api/user_files")
    test.process()
    pprint(test.get_dependencies())
