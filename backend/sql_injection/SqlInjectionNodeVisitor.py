import ast


class SqlInjectionNodeVisitor(ast.NodeVisitor):

    def generic_visit(self, node):
        global isInExpr
        if isinstance(node, ast.Expr):
            #print(f'entering {ast.dump(node, indent=2)}')
            if isinstance(node.value, ast.Call):
                callNode = node.value
                functionAttributeNode = callNode.func
                funcObj = functionAttributeNode.value.id
                funcAttribute = functionAttributeNode.attr
                if (funcAttribute == 'execute'):
                    print("sql execute line found, at line" +
                          str(functionAttributeNode.lineno))
        super().generic_visit(node)
