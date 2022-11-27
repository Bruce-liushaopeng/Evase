import ast
from typing import List
from parseFile import is_query_vulnerable


class SqlInjectionNodeVisitor(ast.NodeVisitor):
    # cursor_name = None
    # sql_package_names = ["sqlite3", "mysql"]
    def __init__(self, marked_sql):
        self.execute_funcs = {}
        self.current_func_scope = None
        self.current_func_node = None
        self.lst_of_assignments = []
        self.marked_sql = marked_sql

    def assign_parent_nodes(self, root_module: ast.Module):
        setattr(root_module, 'parent', None)
        for node in ast.walk(root_module):
            for child in ast.iter_child_nodes(node):
                setattr(child, 'parent', node)
        return

    def get_execute_funcs(self) -> List[str]:
        return self.execute_funcs

    def generic_visit(self, node: ast.AST):

        if isinstance(node, ast.Assign):
            self.lst_of_assignments.append(node)

        if isinstance(node, ast.Expr):
            print("Found expression node, finding parent node")

            if isinstance(node.value, ast.Call):
                print(ast.dump(node, indent=2))
                call_node = node.value
                func_args = call_node.args
                if len(call_node.args) > 0:
                    arg_list = []
                    args = call_node.args[0]
                    for x in ast.walk(args):
                        if hasattr(x, "id"):
                            arg_list.append(x.id)

                    print("calling sql")
                # call_node.args gives the arguments in a function call
                function_attribute_node = call_node.func
                func_obj = function_attribute_node.value.id
                func_attribute = function_attribute_node.attr
                print("FUNCTION ATTRIBUTE: " + func_attribute)
                if func_attribute == 'execute':
                    # print(
                    #     f"sql execute line found at line  {str(function_attribute_node.lineno)}, within function {self.currentFunc}")
                    lst = reversed(self.lst_of_assignments.copy())
                    print("calling check on call_node11")
                    self.marked_sql.vulnerableVariables(
                        lst, self.current_func_node, arg_list)
                    print("calling check on call_node22")
                    self.execute_funcs[self.current_func_scope] = self.current_func_node
                    print("calling check on call_node")
                    is_query_vulnerable(call_node)

        super().generic_visit(node)

    def visit_FunctionDef(self, node: ast.AST):
        print("--------------")
        # keep track of the function block we are in
        print("visiting " + node.name)
        self.current_func_scope = node.name
        self.current_func_node = node
        self.lst_of_assignments = []
        super().generic_visit(node)
