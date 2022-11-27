import ast


class SqlMarked:

    def vulnerableVariables(self, list_of_assignments: list, func_node, list_of_variables):

        print("here inside vulnerable ----------")
        parameters = self.get_parameter_args(func_node)
        marked_variables = set(list_of_variables)
        print(marked_variables)
        for assignment in list_of_assignments:
            print("Assignment")
            for target in assignment.targets:
                print(ast.dump(target, indent=2))
                if hasattr(target, "id"):
                    print("id block")
                    print("take out variable" + target.id)
                elif hasattr(target, "elts"):
                    print("elts block")
                    for val in target.elts():
                        if hasattr(val, "id"):
                            print("take out variable" + val.id)
                print("walk")
                # print(ast.dump(x))
            print("-----")

            #print(ast.dump(assignment, indent=2))

    def get_parameter_args(self, node):
        set_of_parameters = set()
        args = node.args.args
        for arg in args:
            set_of_parameters.add(arg.arg)
        return set_of_parameters
