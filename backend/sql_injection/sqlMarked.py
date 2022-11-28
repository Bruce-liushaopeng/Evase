import ast


class SqlMarked:

    def vulnerableVariables(self, list_of_assignments: list, func_node, list_of_variables):
        print("here inside vulnerable ----------")
        parameters = self.get_parameter_args(func_node)
        marked_variables = set(list_of_variables)
        print(marked_variables)
        for assignment in reversed(list_of_assignments):
            print("Assignment")
            print(ast.dump(assignment, indent=2))

            target_lst = []
            for target in assignment.targets:
                if hasattr(target, "id"):
                    target_lst.append(target.id)
                elif hasattr(target, "elts"):
                    for val in target.elts:
                        if hasattr(val, "id"):
                            target_lst.append(val.id)

            print(target_lst)

            val_lst = []
            if hasattr(assignment.value, "elts"):
                for x in assignment.value.elts:
                    lst = []
                    for y in ast.walk(x):
                        if hasattr(y, "id"):
                            lst.append(y.id)

                    val_lst.append(lst.copy())
            else:
                lst = []
                for y in ast.walk(assignment.value):
                    if hasattr(y, "id"):
                        lst.append(y.id)
                val_lst.append(lst)

            print(val_lst)


    def get_parameter_args(self, node):
        set_of_parameters = set()
        args = node.args.args
        for arg in args:
            set_of_parameters.add(arg.arg)
        return set_of_parameters
