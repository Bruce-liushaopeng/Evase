class FileStruct:

    def __init__(self, ast_file):
        self.module_uses = dict()
        self.func_uses = dict()
        self.class_uses = dict()
        self.method_uses = dict()
        self.ast_file = ast_file

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
