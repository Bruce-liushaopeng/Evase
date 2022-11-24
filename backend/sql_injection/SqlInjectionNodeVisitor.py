import ast
from pprint import pprint
from parseFile import isSqlStatementVunerable


class SqlInjectionNodeVisitor(ast.NodeVisitor):
    # cursor_name = None
    # sql_package_names = ["sqlite3", "mysql"]

<<<<<<< HEAD
    def assign_parent_nodes(self, root_module:ast.Module):
=======
    def __init__(self):
        self.funcDict = {}
        self.currentFunc = None
        self.currentFuncNode = None
        self.problemFunctions = {}  # functionName : FunctionNode

    def assign_parent_nodes(self, root_module: ast.Module):
>>>>>>> bruce-dev
        setattr(root_module, 'parent', None)
        for node in ast.walk(root_module):
            for child in ast.iter_child_nodes(node):
                setattr(child, 'parent', node)
        return root_module

    def generic_visit(self, node):
        if isinstance(node, ast.Expr):
            print("Found expression node, finding parent node")
            parent_node = node.parent
            print("Parent: ", parent_node.__class__)

            try:
                if isinstance(node.value, ast.Call):
                    callNode = node.value
                    funcArgs = callNode.args
                    # callNode.args gives the arguments in a function call
                    functionAttributeNode = callNode.func
                    funcObj = functionAttributeNode.value.id
                    funcAttribute = functionAttributeNode.attr

                    if (funcAttribute == 'execute'):
                        # print(
                        #     f"sql execute line found at line  {str(functionAttributeNode.lineno)}, within function {self.currentFunc}")
                        self.problemFunctions[self.currentFunc] = self.currentFuncNode
                        print("calling check on callNode")
                        isSqlStatementVunerable(callNode)

            except:
                # attribute not found, could be optimized with diff approach other than try exept.
                spaceholder = "spaceholder"

        super().generic_visit(node)

    def visit_FunctionDef(self, node):
        # keep track of the function block we are in
        print("visiting " + node.name)
        self.currentFunc = node.name
        self.currentFuncNode = node
        super().generic_visit(node)
