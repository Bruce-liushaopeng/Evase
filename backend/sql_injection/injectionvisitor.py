from parseFile import is_query_vulnerable
from typing import List, Dict, Any
import ast
import sys
from injectionutil import SqlMarker, get_all_vars


class InjectionNodeVisitor(ast.NodeVisitor):
    # cursor_name = None
    # sql_package_names = ["sqlite3", "mysql"]
    def __init__(self):
        self.execute_funcs = {}
        self.current_func_node = None
        self.lst_of_assignments = []
        self.sql_marker = SqlMarker()

    def get_execute_funcs(self) -> dict[Any, Any]:
        return self.execute_funcs

    def visit_Expr(self, node: ast.Expr):
        super().generic_visit(node)

    def visit_Assign(self, node: ast.Assign):
        self.lst_of_assignments.append(node)
        super().generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef):
        self.current_cls_node = node
        super().generic_visit(node)

    def visit_Call(self, node: ast.Call):
        if node.func.attr == "execute":
            self.visit_execute(node)
        super().generic_visit(node)

    def visit_execute(self, node: ast.Call):
        lst = self.lst_of_assignments.copy()
        arg_list = get_all_vars(node)

        curr_scope = self.get_current_scope()
        print("EXEC found, curr scope:", curr_scope)
        print(self.current_func_node.parent_classes)

        print(self.sql_marker.collect_vulnerable_vars(
            lst, self.current_func_node, arg_list))
        self.execute_funcs[curr_scope] = self.current_func_node

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self.current_func_node = node
        self.lst_of_assignments = []
        super().generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        self.visit_FunctionDef()

    def get_current_scope(self):
        if self.current_func_node:
            return self.current_func_node.name
        else:
            return ""


if __name__ == '__main__':
    anyone = InjectionNodeVisitor()
