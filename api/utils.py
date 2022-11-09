# The purpose of this module is to provide functions
# for the data structures

import ast
import os

def parseInformation(tree: ast):
    fns = {}
    dep = {}

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for modl in node.names:
                dep[modl.name] = {
                    "as": modl.asname,
                    "funcs": []
                }
        elif isinstance(node, ast.ImportFrom):
            if node.module in dep:
                dep[node.module]['funcs'].extend([(fn.name, fn.asname) for fn in node.names])
            else:
                dep[node.module] = {
                    "as": None,
                    "funcs": [(fn.name, fn.asname) for fn in node.names]
                }
        elif isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
            fns[node.name] = node.body

    return dep, fns

class Module:

    def __init__(self, path: str, tree: ast):
        self.name = ".".join(path.split(os.sep)[1:])    # put it in package format
        self.tree = tree
        
        dep, fns = parseInformation(tree)

        self.dependencies = dep
        self.functions = fns

    def getName(self) -> str:
        return self.name

    def getDependcies(self) -> dict:
        return self.dependencies

    def getFunctions(self) -> dict:
        return self.functions

    def getTree(self):
        return self.tree

    def __eq__(self, __o: object) -> bool:
        if (isinstance(__o, Module)):
            return __o.name == self.name
        return False


def readDir(dirstr: str):
    if not os.path.exists(dirstr):
        return

    modules = []

    for (dirpath, dirnames, filenames) in os.walk(dirstr):
        for f in filenames:
            relpath = os.path.join(dirpath, f)
            header, ext = os.path.splitext(f)
            with open(relpath, "r") as file:
                if ext == ".py":
                    mod = Module(relpath, ast.parse(file.read()))
                    modules.append(mod)
                
    return modules

if __name__ == '__main__':
    readDir("user file")
    
