from typing import List, Dict, Any
import ast
from backend.sql_injection.injectionutil import SqlMarker, get_all_vars


class InjectionNodeVisitor(ast.NodeVisitor):
    # cursor_name = None
    # sql_package_names = ["sqlite3", "mysql"]
    def __init__(self):
        self.execute_funcs = {}
        self.current_func_node = None
        self.lst_of_assignments = []
        self.sql_marker = SqlMarker()
        self.if_flag = True

    def get_execute_funcs(self) -> dict[Any, Any]:
        return self.execute_funcs

    def visit_Expr(self, node: ast.Expr):
        super().generic_visit(node)

    def visit_Assign(self, node: ast.Assign):
        print(ast.dump(node))
        self.lst_of_assignments.append(node)
        super().generic_visit(node)

    def visit_If(self, node: ast.If):
        if self.if_flag:
            self.lst_of_assignments.append("if")
        for val in node.body:
            self.visit(val)

        if len(node.orelse) > 0:
            prev = self.if_flag
            self.if_flag = False
            self.else_visit(node.orelse)
            self.if_flag = prev

        if self.if_flag:
            self.lst_of_assignments.append("endif")


    def else_visit(self, nodes):
        if len(nodes) == 0:
            self.lst_of_assignments.append("endelse")
        else:
            self.lst_of_assignments.append("else")
            for node in nodes:
                self.visit(node)

    def visit_While(self, node: ast.While) -> Any:
        self.lst_of_assignments.append("while")
        super().generic_visit(node)
        self.lst_of_assignments.append("endwhile")

    def visit_For(self, node: ast.For) -> Any:
        self.lst_of_assignments.append("for")
        super().generic_visit(node)
        self.lst_of_assignments.append("endfor")

    def visit_Return(self, node: ast.Return) -> Any:
        self.lst_of_assignments.append(node)
        super().generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef):
        self.current_cls_node = node
        super().generic_visit(node)

    def visit_Call(self, node: ast.Call):
        if hasattr(node.func, "attr") and node.func.attr == "execute":
            print(self.lst_of_assignments)
            self.visit_execute(node)
        super().generic_visit(node)

    def visit_execute(self, node: ast.Call):
        lst = self.lst_of_assignments.copy()
        arg_list = get_all_vars(node.args[0])
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
        self.visit_FunctionDef(node)

    def get_current_scope(self):
        if self.current_func_node:
            return self.current_func_node.name
        else:
            return ""


if __name__ == '__main__':
    anyone = InjectionNodeVisitor()
