import ast
from ast2json import str2json
import json
import inspect
import os


class AnalysisNodeVisitor(ast.NodeVisitor):
    def __init__(self, base_dir):
        self.base_dir = base_dir

    def visit_ImportFrom(self, node, msg):
        ast.NodeVisitor.generic_visit(self, node)

    def visit_ImportFrom(self, node):
        if self.base_dir not in node.module:
            print(self.base_dir+"."+node.module + " module")
        else:
            print(node.module + " module")

        ast.NodeVisitor.generic_visit(self, node)

"""
    def visit_FunctionDef(self, node):
        print('Node type: visit_FunctionDef: ', node._fields, node._attributes)
        print(node.name, node.args, node.body, " here\n")
        print(inspect.getfile(node.name().__class__))
        ast.NodeVisitor.generic_visit(self, node)

    def visit_ImportFrom(self, node):
        for alias in node.names:
            print(alias.name)
            #inspect.getsource(alias.name)
        print('Node type: visit_ImportFrom: ', node._fields, node._attributes)
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Import(self, node):
        for alias in node.names:
            print(alias.name, ' import')
        print('Node type: visit_ImportFrom: ', node._fields, node._attributes)
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Assign(self, node):
        # for alias in node.value:
        #     print(alias.name, ' import')
        print('Node type: Assign and fields: ', node._fields, node.value, node.targets)
        ast.NodeVisitor.generic_visit(self, node)

    def visit_BinOp(self, node):
        print('Node type: BinOp and fields: ', node._fields, node._attributes)
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Expr(self, node):
        print('Node type: Expr and fields: ', node._fields, node._attributes)
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Num(self, node):
        print('Node type: Num and fields: ', node._fields, node.value, node.kind)

    def visit_Name(self, node):
        print('Node type: Name and fields: ', node._fields, node.id, node.ctx)
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Str(self, node):
        print('Node type: Str and fields: ', node._fields, node._attributes)
"""


def iter(dir, imp):
    with os.scandir(dir) as it:
        for entry in it:
            if entry.is_dir():
                iter(dir + "/" + entry.name, imp + "." + entry.name)
            elif entry.name.endswith('.py') and entry.is_file() and entry.name != "parse.py":
                name = entry.name[:len(entry.name) - 3]
                print(entry.name + " " + imp + "." + name)
                print(dir + "/" + entry.name)
                f = open(dir + "/" + entry.name, "r")
                k = ast.parse(f.read())
                v = AnalysisNodeVisitor(imp)
                v.generic_visit(k)
                f.close()


if __name__ == '__main__':
    iter("/api/depanalyze/src", "src")
    # f = open("test.py", "r")

    # print(ast.dump(ast.parse(f.read()), indent=4))
    # f.close()
    # print("\n here")

    print(json.dumps(str2json(open("test.py").read()), indent=4))

    # print("\n")
    # f = open("test.py", "r")
    # print(f.read());

    # k = ast.parse(f.read())
    # f.close()
    # v = AnalysisNodeVisitor()
    # v.generic_visit(k)

    # print(ast.dump(ast.parse(f.read()), indent=4))
    # print(ast.dump(ast.parse(f2.read()), indent=4))
