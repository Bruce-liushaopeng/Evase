from typing import Dict, List

import ast
import ast_scope
from networkx import DiGraph


class ModuleAnalysisStruct:

    def __init__(self, ast_tree: ast.AST):
        """
        A structure for the easier analysis of a single code module.
        Contains properties of the module such as scoping information.
        Initialize a module analysis structure with a tree.

        :param ast_tree: The ast of the module
        """
        self.ast_tree = ast_tree
        self.scope_info = None
        self.static_dep = None
        self.static_uses = None
        self.process()

    def process(self):
        """
        Process the tree and determine scopes.
        """
        self.scope_info = ast_scope.annotate(self.ast_tree)
        self.static_dep = self.scope_info.static_dependency_graph
        uses = {}
        for item in self.static_dep.edges():
            if item[0] not in uses:
                uses[item[0]] = []
            uses[item[0]].append(item[1])
        self.static_uses = uses

    def get_ast(self) -> ast.AST:
        """
        Retrieve the internal ast tree.

        :return: ast for the module
        """
        return self.ast_tree

    def get_scope_info(self):
        """
        Get the scope information object (ast_scope).

        :return: Scope information for current module
        """
        return self.scope_info

    def get_scope_of_node(self, node: ast.AST):
        """
        THIS IS THE KICKER.
        Get the scope information object (ast_scope) for a specific node.

        :param node: The node for which to obtain scope
        :return: The scope information for the node
        """
        return self.scope_info[node]

    def get_static_uses(self) -> Dict[ast.AST, List[ast.AST]]:
        """
        Get a mapping of use edges: nodes to use nodes (only in the same module).

        main() calls foo() and bar().
        {
            Node of main(): [Node of foo(), Node of bar()]
        }

        :return: The use edges of the current AST tree
        """

        return self.static_uses

    def get_static_deps(self) -> DiGraph:
        """
        Get the static dependency graph (equivalent to get_static_uses).

        :return: Graph object representation of use edges
        """
        return self.static_dep
