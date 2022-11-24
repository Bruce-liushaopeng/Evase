import ast
from pprint import pprint
from backend.depanalyze.modulestructure import ModuleAnalysisStruct

class SqlInjectionNodeVisitor(ast.NodeVisitor):
    # cursor_name = None
    # sql_package_names = ["sqlite3", "mysql"]

    def __init__(self, module_name, ast_tree):
        self.analysis_structure = ModuleAnalysisStruct(module_name, ast_tree)

    def process(self):
        self.generic_visit(self.analysis_structure.get_ast())

    def assign_parent_nodes(self, root_module:ast.Module):
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
                    
                    # callNode.args gives the arguments in a function call
                    functionAttributeNode = callNode.func
                    funcObj = functionAttributeNode.value.id
                    funcAttribute = functionAttributeNode.attr

                    if (funcAttribute == 'execute'):
                        # print(
                        #     f"sql execute line found at line  {str(functionAttributeNode.lineno)}, within function {self.currentFunc}")
                        self.problemFunctions[self.currentFunc] = self.currentFuncNode
            except:
                # attribute not found, could be optimized with diff approach other than try exept.
                spaceholder = "spaceholder"
        
        super().generic_visit(node)

    def visit_FunctionDef(self, node):
        # keep track of the function block we are in
        print("visiting " + node.name)
        self.currentFunc = node.name
        self.currentFuncNode = node
        self.generic_visit(node)
