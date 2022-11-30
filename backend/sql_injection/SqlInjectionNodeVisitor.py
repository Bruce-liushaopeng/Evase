from parseFile import is_query_vulnerable
from typing import List
import ast
import sys
from injectionutil import SqlMarker, get_all_vars

class SqlInjectionNodeVisitor(ast.NodeVisitor):
    # cursor_name = None
    # sql_package_names = ["sqlite3", "mysql"]
    def __init__(self):
        self.execute_funcs = {}
        self.current_cls_node = None
        self.current_func_scope = None
        self.current_func_node = None
        self.lst_of_assignments = []
        self.sql_marker = SqlMarker()

    def get_execute_funcs(self) -> List[str]:
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

        print("SCOPE OF EXEC:", self.get_current_scope())
        print(self.sql_marker.collect_vulnerable_vars(
            lst, self.current_func_node, arg_list))
        self.execute_funcs[self.current_func_scope] = self.current_func_node

    def verify_cls(self):
        if self.current_cls_node:
            found = False
            for node in ast.walk(self.current_cls_node):
                if node == self.current_func_node:
                    found = True

            if not found:
                self.current_cls_node = None

    def verify_fn(self, node: ast.AST):
        found = False
        for cnode in ast.walk(self.current_func_node):
            if cnode == node:
                found = True

        if not found:
            self.current_func_node = None

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self.current_func_node = node
        self.verify_cls()
        self.lst_of_assignments = []
        super().generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        self.visit_FunctionDef()

    def get_current_scope(self):
        if self.current_cls_node:
            if self.current_func_node:
                return f'{self.current_cls_node.name}.{self.current_func_node.name}'
            else:
                return self.current_cls_node.name
        if self.current_func_node:
            return self.current_func_node.name
        return ""


if __name__ == '__main__':
    anyone = SqlInjectionNodeVisitor()
