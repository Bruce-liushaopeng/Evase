import ast
import os
from pprint import pprint


class InjectionDetectionVisitor(ast.NodeVisitor):

    def __init__(self):
        self.statement_stack = []
        self.scope_stack = []

        self.info_tree = {
            "functions": {},
            "dependencies": {},
            "classes": {},
            "globals": {}
        }
        self.fns = self.info_tree['functions']
        self.dep = self.info_tree['dependencies']
        self.clss = self.info_tree['classes']
        self.glbls = self.info_tree['globals']

    def reset(self):
        self.statement_stack.clear()
        self.scope_stack.clear()

    @classmethod
    def printScopeNode(node: ast.AST):
        info = {
            'type': type(node),
            'lineno': "unk"
        }
        if any(isinstance(node, t) for t in [ast.FunctionDef, ast.AsyncFunctionDef, ast.For, ast.AsyncFor, ast.With, ast.AsyncWith]):
            info.lineno = node.lineno
        
        print("New scope encountered:")
        pprint(info)

    def add_scope_to_stack(self, node):
        while not isinstance(node, type(self.scope_stack[0])) and len(self.scope_stack) > 0:
            self.scope_stack.pop()
        self.scope_stack.insert(0, node)

    def get_node_scope(self):
        return self.scope_stack[0]

    def visit_ClassDef(self, node):
        InjectionDetectionVisitor.printScopeNode(node)
        self.add_scope_to_stack(node)

    def visit_FunctionDef(self, node):
        InjectionDetectionVisitor.printScopeNode(node)
        self.add_scope_to_stack(node)
        # not this simple, need to find if it belongs to a class or to another function
        inclass = False
        for item in self.scope_stack:
            if isinstance(item, ast.ClassDef):
                self.fns[f'{item.name}.{node.name}'] = node.body
                inclass=True
                break
                
        if not inclass:
            self.fns[node.name] = node.body


    def visit_For(self, node):
        InjectionDetectionVisitor.printScopeNode(node)
        self.add_scope_to_stack(node)

    def visit_AsyncFor(self, node):
        InjectionDetectionVisitor.printScopeNode(node)
        self.add_scope_to_stack(node)

    def visit_With(self, node):
        InjectionDetectionVisitor.printScopeNode(node)
        self.add_scope_to_stack(node)

    def visit_AsyncWith(self, node):
        InjectionDetectionVisitor.printScopeNode(node)
        self.add_scope_to_stack(node)

    def visit_Assign(self, node):
        # for alias in node.value:
        #     print(alias.name, ' import')
        print('Node type: Assign and fields: ', node._fields, node.value, node.targets)
        ast.NodeVisitor.generic_visit(self, node)

    def visit_BinOp(self, node):
        print('Node type: BinOp and fields: ', node._fields, node._attributes)
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Expr(self, node):
        print('Node type: Expr and fields: ', node._fields, node._attributes)
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Num(self, node):
        print('Node type: Num and fields: ', node._fields, node.value, node.kind)

    def visit_Name(self, node):
        print('Node type: Name and fields: ', node._fields, node.id, node.ctx)
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Str(self, node):
        print('Node type: Str and fields: ', node._fields, node._attributes)