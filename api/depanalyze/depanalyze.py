from typing import Dict, List
import ast

import pyan
from pyan.node import Flavor
from glob import glob
import os
from file_struct import ModuleAnalysisStruct
from pprint import pprint
import code2flow

def _get_dependency_relations(dirpath: str):
    filenames = glob(os.path.join(dirpath, '**/*.py'), recursive=True)

    v = pyan.CallGraphVisitor(filenames)

    # collect and sort defined nodes
    defines_edges = []
    uses_edges = []
    visited_nodes = []
    for name in v.nodes:
        for node in v.nodes[name]:
            if node.defined:
                visited_nodes.append(node)

    for n in v.defines_edges:
        for n2 in v.defines_edges[n]:
                defines_edges.append((n, n2))

    for n in v.uses_edges:
        for n2 in v.uses_edges[n]:
                uses_edges.append((n, n2))

    deps = {}

    for node, use in uses_edges:
        if node.get_name() not in deps:
            deps[node.get_name()] = []

        deps[node.get_name()].append(use.get_name())

    return deps

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

    @classmethod
    def dir_to_module_structure(cls, dirpath: str) -> Dict[str, ModuleAnalysisStruct]:
        """
        Converts a directory into a mapping of package style names to module analysis structures

        :param dirpath: The path to the directory of the code
        :return: A mapping of module names to analysis structures
        """
        tree = {}

        namesp = dirpath
        if "__init__.py" in os.listdir(dirpath):  # check if the start path itself is a package
            namesp = os.sep.join(dirpath.split(os.sep)[:-1])

        for root, dirs, files in os.walk(dirpath):
            for f in files:
                fullpath = os.path.join(root, f)
                filename, ext = os.path.splitext(fullpath)
                if ext == ".py":
                    module_style = filename.replace(namesp + os.sep, '').replace(os.sep, '.')
                    with open(fullpath, "r") as fr:
                        tree[module_style] = ModuleAnalysisStruct(ast.parse(fr.read()))

        return tree

    def process(self):
        self._module_structure = ProjectAnalysisStruct.dir_to_module_structure(self._prj_root)
        self._dependencies = _get_dependency_relations(self._prj_root)

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




def _dir_to_module_struct(dirpath: str) -> dict:
    ast_trees = dict()
    _iter_recursive(dirpath, "", ast_trees)
    return ast_trees


def _iter_recursive(dirpath: str, root: str, ast_trees: dict):
    with os.scandir(dirpath) as it:
        for entry in it:
            if entry.is_dir():
                _iter_recursive(dirpath + "/" + entry.name, root + "." + entry.name, ast_trees)

            elif entry.name.endswith('.py') and entry.is_file():
                name, _ = os.path.splitext(entry.name)
                print(entry.name + " " + root + "." + name + " " + dirpath + "/" + entry.name)
                with open(dirpath + "/" + entry.name, "r") as f:
                    ast_file = ast.parse(f.read())
                    ast_trees[root + "." + name] = ModuleAnalysisStruct(ast_file)



if __name__ == '__main__':
    test = ProjectAnalysisStruct("EvaseTest", "C:/courses/SYSC_4907/Evase/api/User File")
    test.process()
    pprint(test.get_dependencies())
