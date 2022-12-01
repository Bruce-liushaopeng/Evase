from typing import Dict, List
import ast
import ast_scope
from networkx import DiGraph

from backend.depanalyze.scoperesolver import ScopeResolver


class ModuleAnalysisStruct:

    def __init__(self, module_name: str, ast_tree: ast.AST):
        """
        A structure for the easier analysis of a single code module.
        Contains properties of the module such as scoping information.
        Initialize a module analysis structure with a tree.

        :param ast_tree: The ast of the module
        """
        self.module_name = module_name
        self.ast_tree = ast_tree
        self.local_imports = {}
        self.module_imports = {}

    def process(self, scope_resolver: ScopeResolver):
        scope_resolver.visit(self.ast_tree)

    def get_name(self):
        return self.module_name

    def get_ast(self) -> ast.AST:
        """
        Retrieve the internal ast tree.
    def get_ast(self) -> ast.AST:
        :return: ast for the module
        """
        return self.ast_tree

    def set_ast(self, ast):
        self.ast_tree = ast

    def get_local_imports(self):
        return self.local_imports

    def set_local_imports(self, local_imports):
        self.local_imports = local_imports

    def get_module_imports(self):
        return self.module_imports

    def set_module_imports(self, module_imports):
        self.module_imports = module_imports