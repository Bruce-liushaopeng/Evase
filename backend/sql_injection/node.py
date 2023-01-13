class Node:
    def __init__(self, func_node, assignments, injection_vars, module_name):
        self.func_node = func_node
        self.assignments = assignments
        self.injection_vars = injection_vars
        self.module_name = module_name

    def get_func_node(self):
        return self.func_node

    def get_assignments(self):
        return self.assignments

    def get_injection_vars(self):
        return self.injection_vars

    def get_module_name(self):
        return self.module_name