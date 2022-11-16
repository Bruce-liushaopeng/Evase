from typing import Dict, List
import ast

import pyan
from pyan.node import Flavor
from glob import glob
import os
from modulestructure import ModuleAnalysisStruct
from pprint import pprint
import code2flow


def get_dependency_relations(dirpath: str):
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
