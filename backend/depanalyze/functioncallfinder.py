import ast

from backend.depanalyze.node import Node
from backend.sql_injection.injectionutil import get_all_vars


class FunctionCallFinder(ast.NodeVisitor):
    def __init__(self, module, module_as_name = None, funcName = None):
        self.module = module
        self.module_as_name = module_as_name
        self.funcName =  funcName
        self.currentFuncNode = None # non important, just keep track
        self.currentFuncScope = None
        self.found_calling_lst = [] # List for storing all the parent function of the vulnerable function

        self.lst_of_assignments = []
        self.if_flag = True

    def generic_visit(self, node):
        
        if (isinstance(node, ast.Expr)):
            lineOfCalling = node.lineno
            callNode = node.value
            if isinstance(callNode, ast.Call):
                if not self.module_as_name:
                    calling_function_name = ""
                    if isinstance(callNode.func, ast.Attribute) :
                        calling_function_name = callNode.func.attr
                    else:
                        calling_function_name = callNode.func.id

                    if (calling_function_name == self.funcName):
                        self.found_calling_lst.append(Node(self.currentFuncNode, self.lst_of_assignments.copy(), [], self.module))
                else:
                    attrbuteNode = callNode.func
                    calling_module_name = attrbuteNode.value.id
                    calling_function_name = attrbuteNode.attr
                    if calling_function_name == self.funcName and calling_module_name == self.module_as_name:
                        #arg_list = get_all_vars(callNode.args)
                        #print(arg_list)
                        self.found_calling_lst.append(Node(self.currentFuncNode, self.lst_of_assignments.copy(), [], self.module))


        super().generic_visit(node)
        return node

    def visit_FunctionDef(self, node: ast.Expr):
        self.currentFuncScope = node.name
        self.currentFuncNode = node
        self.lst_of_assignments = []
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

    def visit_While(self, node: ast.While):
        self.lst_of_assignments.append("while")
        super().generic_visit(node)
        self.lst_of_assignments.append("endwhile")

    def visit_For(self, node: ast.For):
        self.lst_of_assignments.append("for")
        super().generic_visit(node)
        self.lst_of_assignments.append("endfor")

    def visit_Return(self, node: ast.Return):
        self.lst_of_assignments.append(node)
        super().generic_visit(node)


