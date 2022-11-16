from typing import Dict, List
import ast
import re

import pyan
from glob import glob
import os
from modulefinder import ModuleFinder
from modulestructure import ModuleAnalysisStruct


def get_dependency_relations(dirpath: str) -> Dict[str, List[str]]:
    """
    Using Pyan3 to convert a directory into a dependency/call graph.

    :param dirpath: The path to the directory
    :return: The mapping of use edges
    """
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


def dir_to_module_structure(dirpath: str) -> Dict[str, ModuleAnalysisStruct]:
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

def find_star_imports(path: str):
    """
    Find the star imports for a python file

    :param path:
    :return:
    """
    imp_lst = []
    if path.endswith(".py"):
        patt = re.compile(r"from\s((.?\w+.?)+)\simport\s\*")
        with open(path, "r") as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if line == "\n":
                    continue
                if line.endswith('*\n') or line.endswith('*'):
                    match = patt.match(line)
                    if match:
                        imp_lst.append(match.group(1))
    return imp_lst

if __name__ == '__main__':
    print(find_star_imports("C:/courses/SYSC_4907/Evase/backend/user_files/src/test.py"))
