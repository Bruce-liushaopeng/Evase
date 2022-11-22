import ast


class SqlInjectionNodeVisitor(ast.NodeVisitor):

    def __init__(self):
        self.funcDict = {}
        self.currentFunc = None
        self.currentFuncNode = None
        self.problemFunctions = {}  # functionName : FunctionNode

    def generic_visit(self, node):
        # visiting each node, top to buttom, left to right.
        if isinstance(node, ast.Expr):
            try:
                #print(f'entering {ast.dump(node, indent=2)}')
                if isinstance(node.value, ast.Call):
                    callNode = node.value
                    functionAttributeNode = callNode.func
                    funcObj = functionAttributeNode.value.id
                    funcAttribute = functionAttributeNode.attr
                    if (funcAttribute == 'execute'):
                        print(
                            f"sql execute line found at line  {str(functionAttributeNode.lineno)}, within function {self.currentFunc}")
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
