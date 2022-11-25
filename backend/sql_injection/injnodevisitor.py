import ast
from typing import List
from injectionutil import is_query_vulnerable


class SqlInjectionNodeVisitor(ast.NodeVisitor):
    # cursor_name = None
    # sql_package_names = ["sqlite3", "mysql"]
    def __init__(self):
        self.execute_funcs = []
        self.current_func_scope = None
        self.current_func_node = None

    def assign_parent_nodes(self, root_module: ast.Module):
        setattr(root_module, 'parent', None)
        for node in ast.walk(root_module):
            for child in ast.iter_child_nodes(node):
                setattr(child, 'parent', node)
        return

    def get_execute_funcs(self) -> List[str]:
        return self.execute_funcs

    def generic_visit(self, node: ast.AST):
        if isinstance(node, ast.Expr):
            print("Found expression node, finding parent node")
            #parent_node = node.parent
            #print("Parent: ", parent_node.__class__)

            try:
                if isinstance(node.value, ast.Call):
                    call_node = node.value
                    func_args = call_node.args
                    # call_node.args gives the arguments in a function call
                    function_attribute_node = call_node.func
                    func_obj = function_attribute_node.value.id
                    func_attribute = function_attribute_node.attr

                    if func_attribute == 'execute':
                        # print(
                        #     f"sql execute line found at line  {str(function_attribute_node.lineno)}, within function {self.currentFunc}")
                        self.execute_funcs[self.current_func_scope] = self.current_func_scope
                        print("calling check on call_node")
                        is_query_vulnerable(call_node)

            except:
                # attribute not found, could be optimized with diff approach other than try exept.
                spaceholder = "spaceholder"

        super().generic_visit(node)

    def visit_FunctionDef(self, node: ast.AST):
        # keep track of the function block we are in
        print("visiting " + node.name)
        self.current_func_scope = node.name
        self.current_func_node = node
        super().generic_visit(node)
