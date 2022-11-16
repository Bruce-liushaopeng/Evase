import ast_scope
from networkx import DiGraph

class ModuleAnalysisStruct:

    def __init__(self, ast_file):
        self.module_uses = dict()
        self.func_uses = dict()
        self.class_uses = dict()
        self.method_uses = dict()
        self.ast_file = ast_file
        self.uses = None
        self.scope_info = None
        self.static_dep = None

    def process(self):
        self.scope_info = ast_scope.annotate(self.ast_file)
        self.static_dep = self.scope_info.static_dependency_graph
        uses = {}
        for item in self.static_dep.edges():
            if item[0] not in uses:
                uses[item[0]] = []
            uses[item[0]].append(item[1])
        self.static_dep = uses

    def get_ast(self):
        return self.ast_file

    def set_module_uses(self, uses):
        self.uses = uses

    def get_module_uses(self):
        return self.uses

    def set_func_uses(self, func_uses):
        self.func_uses = func_uses

    def get_func_uses(self):
        return self.func_uses

    def set_class_uses(self, uses):
        self.uses = uses

    def get_class_uses(self):
        return self.uses

    def set_method_uses(self, uses):
        self.uses = uses

    def get_method_uses(self):
        return self.uses

    def get_static_deps(self) -> DiGraph:
        return self.static_dep
