from typing import Dict, List
import ast
import re

import pyan
from glob import glob
import os
from modulefinder import ModuleFinder
from backend.depanalyze.surfacedetector import SurfaceLevelVisitor
from backend.injection import InjectionDetectionVisitor
from modulestructure import ModuleAnalysisStruct
import subprocess



def get_dependency_relations(dirpath: str, keep_defined: bool = False) -> Dict[str, List[str]]:
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
        if n.defined and keep_defined:
            for n2 in v.defines_edges[n]:
                if n2.defined and keep_defined:
                    defines_edges.append((n, n2))

    for n in v.uses_edges:
        if n.defined and keep_defined:
            for n2 in v.uses_edges[n]:
                if n2.defined and keep_defined:
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


imp_patt = re.compile(r"(from|import)\s((\.*)((\w+\.?)?)+)")


def is_relative_import(rel_import_str: str):

    ic = 0
    for c in rel_import_str:
        if c != '.':
            break
        ic += 1

    return ic


def clean_up_project_imports(root_path: str, asts: Dict[str, ModuleAnalysisStruct]):
    """
    removes redundant and star imports from the python files in the directory

    :param asts:
    :param root: The path to the directory of the code
    """
    detector = SurfaceLevelVisitor()
    for root, dirs, files in os.walk(root_path):
        for f in files:
            fullpath = os.path.join(root, f)
            filename, ext = os.path.splitext(fullpath)
            if ext == ".py":
                print(fullpath)
                resolve_file_imports(root_path, fullpath, asts, detector)
                detector.clear_surface_names()


def resolve_file_imports(root: str, fullpath: str, asts: Dict[str, ModuleAnalysisStruct],
                         detector: SurfaceLevelVisitor):

    subprocess.run(f'absolufy-imports {fullpath} --application-directories {root}')

    seen_imports = set()
    with open(fullpath, "r") as f:
        data = f.readlines()

    print(root, fullpath)

    for i in range(len(data) - 1, -1, -1):


        if data[i].startswith("from ") and data[i][len(data[i]) - 2] == "*":
            parts = data[i].strip("\n").split(" ")
            # do traversal on imported module
            detector.visit(asts[parts[1]])
            lst = unseen_imports(seen_imports, detector.get_surface_names())

        elif data[i].startswith("from "):
            parts = data[i].strip("\n").split(" ")
            lst = unseen_imports(seen_imports, parts[3:len(parts)])

        # ast = dir_to_module_structure("C:/Users/Anthony/Desktop/Desktop/Proj/parser")["src.test"].get_ast()


def unseen_imports(seen_imports: set, imprts: list):
    new_imports = []
    for x in imprts:
        if x not in seen_imports:
            seen_imports.add(x)
            new_imports.append(x)
    return new_imports


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


def fix_relative_imports(paths: str, path: str, alt=False):
    if alt:
        splpath = path.split(os.altsep)
    else:
        splpath = path.split(os.sep)

    if os.path.isabs(path):
        splpath = splpath[1:-1]

    lst = []

    for k in paths:
        print(k)
        ic = 0
        for c in k:
            if c != '.':
                break
            ic += 1
        if ic != 0:
            lst.append('.'.join(splpath[-ic:]) + '.' + k[ic:])
        else:
            lst.append(k)

    return lst


if __name__ == '__main__':
    from pprint import pprint
    pprint(get_dependency_relations(r"U:\courses\SYSC_4907\Evase\backend\user_files"))

    #asts = dir_to_module_structure(r"U:\courses\SYSC_4907\Evase\backend\user_files")
    #clean_up_project_imports(r"U:\courses\SYSC_4907\Evase\backend\user_files", asts)
    # ast = asts["src.test"].get_ast()
    # p.visit(ast)
    # print(p.get_surface_names())
