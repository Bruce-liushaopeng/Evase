from typing import List, Collection
import ast


def get_function_params(node) -> set:
    """
    Finds the set of function parameters from an ast node.

    :param node: An ast node representing a function definition
    :return: The set of the function parameters
    """
    params = set()
    args = node.args.args
    for arg in args:
        params.add(arg.arg)
    return params


class SqlMarker:

    def collect_vulnerable_vars(self, assignment_nodes: List[ast.Assign], func_node,
                                injection_vars: Collection[ast.Name]):
        """
        Collects injection-based vulnerable variables from a function.
        Given a list of nodes corresponding to assignment in the order they are given, the node for the containing
        function, and a list of variables in the potential injection vulnerable statement.

        :param assignment_nodes: The list of assignment nodes inside the function definition
        :param func_node: The node of the function definition
        :param injection_vars: The variables in the potential injection statement
        :return:
        """
        print("here inside vulnerable ----------")
        parameters = get_function_params(func_node)
        marked_variables = set(injection_vars)
        print(marked_variables)
        for assignment in reversed(assignment_nodes):
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
