from typing import List, Collection
import ast


def get_function_params(node) -> set:
    """
    Finds the set of function parameters from an ast node.

    :param node: An ast node representing a function definition
    :return: The set of the function parameters
    """
    params = []
    args = node.args.args
    for arg in args:
        params.append(arg.arg)
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
        parameters = get_function_params(func_node)
        marked_variables = set(injection_vars)
        for assignment in reversed(assignment_nodes):

            target_lst = []         # list of targets for this assignment

            for target in assignment.targets:

                if isinstance(target, ast.Name):
                    target_lst.append(target.id)

                elif hasattr(target, "elts"):
                    for val in target.elts:
                        if hasattr(val, "id"):
                            target_lst.append(val.id)

            val_lst = []            # list of assignment values for each target

            if hasattr(assignment.value, "elts"):
                for x in assignment.value.elts:
                    lst = []
                    for y in ast.walk(x):
                        if isinstance(y, ast.Name):
                            lst.append(y.id)
                    val_lst.append(lst.copy())
            else:
                lst = []
                for y in ast.walk(assignment.value):
                    if isinstance(y, ast.Name):
                        lst.append(y.id)
                val_lst.append(lst)

            for index in range(len(target_lst)-1, -1,-1):
                if target_lst[index] in marked_variables:
                    marked_variables.remove(target_lst[index])
                    for vulnerable_var in val_lst[index]:
                        marked_variables.add(vulnerable_var)

        vulnerable_parameter = []
        for ind in range(0,len(parameters)):
            if parameters[ind] in marked_variables:
                vulnerable_parameter.append(ind)
        return vulnerable_parameter

