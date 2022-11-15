import ast

import pyan
from glob import glob
import os

from typing import Dict

from api.injection import InjectionDetectionVisitor
from file_struct import FileStruct
from pprint import pprint


def _dir_to_module_structure(startpath: str) -> dict:
    tree = {}

    namesp = startpath
    if "__init__.py" in os.listdir(startpath):  # check if the start path itself is a package
        namesp = os.sep.join(startpath.split(os.sep)[:-1])

    for root, dirs, files in os.walk(startpath):
        for f in files:
            fullpath = os.path.join(root, f)
            filename, ext = os.path.splitext(fullpath)
            if ext == ".py":
                module_style = filename.replace(namesp + os.sep, '').replace(os.sep, '.')
                with open(fullpath, "r") as fr:
                    tree[module_style] = FileStruct(ast.parse(fr.read()))

    return tree


class ProjectAnalysisStruct:

    def __init__(self, prj_name: str, prj_root: str):
        self.prj_name = prj_name

        if not os.path.exists(prj_root):
            raise ValueError("Can't accept a file path that doesn't exist.")

        self._prj_root = prj_root
        self.dependencies = {}  # to be kept none? may need it later
        self._module_structure = {}

    def process(self):
        self._module_structure = _dir_to_module_structure(self._prj_root)

    def get_prj_root(self):
        return self._prj_root

    def get_module_structure(self) -> dict:
        return self._module_structure


def _get_dependency_relations():
    filenames = glob(os.path.join(os.path.dirname(__file__), 'src/**/*.py'), recursive=True)
    v = pyan.CallGraphVisitor(filenames)

    # collect and sort defined nodes
    edges = []
    uses_edges = []
    visited_nodes = []
    for name in v.nodes:
        for node in v.nodes[name]:
            if node.defined:
                visited_nodes.append(node)

    for n in v.defines_edges:
        if n.defined:
            for n2 in v.defines_edges[n]:
                if n2.defined:
                    edges.append((n, n2))

    for n in v.uses_edges:
        if n.defined:
            for n2 in v.uses_edges[n]:
                if n2.defined:
                    uses_edges.append((n, n2))

    return [visited_nodes, v, v.uses_edges]


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
                    ast_trees[root + "." + name] = FileStruct(ast_file)


# res = get_dependency_relations()
# print(res[2])
# for node in res[2]:
#    if node.defined:
#        node_name = node.__str__()
#        if "<Node module" in node_name:
#            file_name = node_name.split("<Node module:")[1]
#            file_name = file_name[: len(file_name) - 1]
#
#        elif "<Node function" in node_name:
#            file_name = node_name.split("<Node function:")[1]
#        elif "<Node class" in node_name:
#            file_name = node_name.split("<Node class:")[1]
#        elif "<Node method" in node_name:
#            file_name = node_name.split("<Node method:")[1]
#        print(file_name)
#        print(res[2].get(node))

if __name__ == '__main__':

    pas = ProjectAnalysisStruct("EvaseTest", os.path.join(os.path.dirname(__file__), "src"))
    pas.process()
    pprint(pas.get_module_structure())

    # ast_trees = dir_to_module_struct(os.path.join(os.path.dirname(__file__), "src"))
    # pprint(ast_trees)

    # for x in ast_trees.keys():
    #    print(x)
    #    detector = InjectionDetectionVisitor()
    #    print(ast_trees.get(x).get_ast())
