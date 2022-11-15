import ast

import pyan
from glob import glob
import os

from typing import Dict

from api.injection import InjectionDetectionVisitor
from file_struct import FileStruct
from pprint import pprint

def get_dependency_relations():
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


def dir_to_module_struct(dirpath: str) -> dict:
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



res = get_dependency_relations()
print(res[2])
for node in res[2]:
    if node.defined:
        node_name = node.__str__()
        if "<Node module" in node_name:
            file_name = node_name.split("<Node module:")[1]
            file_name = file_name[: len(file_name) - 1]

        elif "<Node function" in node_name:
            file_name = node_name.split("<Node function:")[1]
        elif "<Node class" in node_name:
            file_name = node_name.split("<Node class:")[1]
        elif "<Node method" in node_name:
            file_name = node_name.split("<Node method:")[1]
        print(file_name)
        print(res[2].get(node))


if __name__ == '__main__':
    ast_trees = dir_to_module_struct(os.path.join(os.path.dirname(__file__), "src"))
    pprint(ast_trees)

    for x in ast_trees.keys():
        print(x)
        detector = InjectionDetectionVisitor()
        print(ast_trees.get(x).get_ast())

