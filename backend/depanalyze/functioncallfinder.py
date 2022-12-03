import ast
import os
from _ast import Module, ImportFrom, ClassDef, FunctionDef
from pathlib import Path


class FunctionCallFinder(ast.NodeVisitor):
    def __init__(self, moduleName = None, funcName = None):
        self.moduleName = moduleName
        self.funcName =  funcName
        self.parentFuncScope = None# important, determine where the func is called within
        self.parentFuncNode = None
        self.currentFuncNode = None # non important, just keep track
        self.currentFuncScope = None
        self.linoFunctionCall = 0

    def generic_visit(self, node):
        
        if (isinstance(node, ast.Expr)):
            lineOfCalling = node.lineno
            callNode = node.value
            print(node.__class__)
            print(callNode.__class__)
            if isinstance(callNode, ast.Call):
                
                if not self.moduleName:
                    print("in if")
                    calling_function_name = callNode.func.id
                    if (calling_function_name == self.funcName):
                        self.linoFunctionCall = lineOfCalling
                        self.parentFuncNode = self.currentFuncNode
                        self.parentFuncScope = self.currentFuncScope
                else:
                    print("in else")
                    attrbuteNode = callNode.func
                    calling_module_name = attrbuteNode.value.id
                    calling_function_name = attrbuteNode.attr
                    if calling_function_name == self.funcName and calling_module_name == self.moduleName:
                        self.linoFunctionCall = lineOfCalling
                        self.parentFuncNode = self.currentFuncNode
                        self.parentFuncScope = self.currentFuncScope


        super().generic_visit(node)
        return node

    def visit_FunctionDef(self, node: ast.Expr):
        self.currentFuncScope = node.name
        self.currentFuncNode = node
        super().generic_visit(node)


