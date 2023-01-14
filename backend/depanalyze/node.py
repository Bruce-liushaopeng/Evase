class Node:
    def __init__(self, func_node, assignments, injection_vars, module_name):
        self._func_node = func_node
        self._assignments = assignments
        self._injection_vars = injection_vars
        self._module_name = module_name

    def get_func_node(self):
        return self._func_node

    def get_assignments(self):
        return self._assignments

    def get_injection_vars(self):
        return self._injection_vars

    def get_module_name(self):
        return self._module_name
