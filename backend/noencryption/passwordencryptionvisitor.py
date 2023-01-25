import json
import ast


with open("passenc-config.json", 'r') as f:
    JSON_CONFIG = json.loads(f.read())


class PasswordEncryptionVisitor(ast.NodeVisitor):
    # cursor_name = None
    # sql_package_names = ["sqlite3", "mysql"]
    def __init__(self, project_struct, module_key):
        print()
        self.project_struct = project_struct
        self.module_key = module_key
        self.hash_calls = []
        self.psswd_uses = []
        self.current_func_node = None

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self.current_func_node = node
        super().generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        self.visit_FunctionDef(node)

    def visit_Call(self, node: ast.Call):
        print()
        super().generic_visit(node)

    def visit_Name(self, node: ast.Name):
        print()
        super().generic_visit(node)


    def get_current_scope(self):
        if self.current_func_node:
            return self.current_func_node.name
        else:
            return ""


if __name__ == '__main__':
    anyone = PasswordEncryptionVisitor()
