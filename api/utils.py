# The purpose of this module is to provide functions
# for the data structures

import ast, os

def parse_syntax_information(tree: ast):
    info_tree = {
        "functions": {},
        "dependencies": {},
        "classes": {},
        "globals": {}
    }
    fns = info_tree['functions']
    dep = info_tree['dependencies']
    clss = info_tree['classes']
    glbls = info_tree['globals']

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
            # not this simple, need to find if it belongs to a class or to another function
            fns[node.name] = node.body


        elif isinstance(node, ast.ClassDef):
            clss[node.name] = node

    return info_tree


class Module:

    def __init__(self, path: str, tree: ast):
        self.name = ".".join(path.split(os.sep)[1:])  # put it in package format
        self.tree = tree

        info_tree = parse_syntax_information(tree)

        self.dependencies = info_tree['dependencies']
        self.functions = info_tree['functions']
        self.classes = info_tree['classes']

    def get_name(self) -> str:
        return self.name

    def get_dependencies(self) -> dict:
        return self.dependencies

    def get_functions(self) -> dict:
        return self.functions

    def get_syntax_tree(self):
        return self.tree

    def get_classes(self):
        return self.classes

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Module):
            return __o.name == self.name
        return False


def directory_to_modules(dirstr: str):
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
    directory_to_modules("user file")
