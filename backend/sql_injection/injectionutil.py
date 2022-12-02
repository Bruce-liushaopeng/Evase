from typing import List, Collection
import ast


def get_function_params(node) -> list:
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


def get_all_targets(node: ast.Assign) -> list:
    """
    Gets all the targets for an assignment.

    :param node: The assignment node
    :return: The list of assignment ids
    """
    target_lst = []

    for target in node.targets:
        if isinstance(target, ast.Name):
            target_lst.append(target.id)

        elif hasattr(target, "elts"):
            for val in target.elts:
                if hasattr(val, "id"):
                    target_lst.append(val.id)

    return target_lst


def get_all_vars(node: ast.AST) -> set:
    """
    Recursively looks at a node and collects the variables used in that node (EXCLUDING THE BODY).

    :param node: The node to look through
    :return: The set of variable ids used inside a node
    """

    args = set()

    # base case 1, stop when the parameter has an ID
    if hasattr(node, "id"):
        args.add(node.id)

    elif hasattr(node, "elts"):
        for subarg in node.elts:
            for subsubarg in get_all_vars(subarg):
                args.add(subsubarg)

    elif isinstance(node, ast.Dict):
        for subarg in node.values:
            for subsubarg in get_all_vars(subarg):
                args.add(subsubarg)

    elif isinstance(node, ast.BinOp):
        for l_subarg in get_all_vars(node.left):
            args.add(l_subarg)
        for r_subarg in get_all_vars(node.right):
            args.add(r_subarg)

    elif hasattr(node, "args"):
        args.add(node)
        #for arg in node.args:
        #    for subarg in get_all_vars(arg):
        #        args.add(subarg)

    elif hasattr(node, "value"):
        for subarg in get_all_vars(node.value):
            args.add(subarg)

    return args


def get_all_target_values(node: ast.Assign) -> list:
    """
    Gets the variables used in the assignment of each target.

    :param node: The assignment node
    :return: The list of values for each target, empty set signifies no variables
    """
    val_lst = []  # collect all variables mentioned for each assignment
    try:
        for val in node.value.elts:
            val_lst.append(get_all_vars(val))
    except AttributeError:
        val_lst.append(get_all_vars(node.value))

    return val_lst


def quicktest():
    tst = ast.parse("password, b, c = a+c, c, '2'")
    for nod in ast.walk(tst):
        if isinstance(nod, ast.Assign):
            print(get_all_vars(nod))


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
        :return: A list which correlates parameter numbers with
        """
        parameters = get_function_params(func_node)
        marked_variables = set(injection_vars)
        for assignment in reversed(assignment_nodes):

            target_lst, val_lst = get_all_targets(assignment), get_all_target_values(assignment)
            print("Assignment TARGETS", target_lst)
            print("Assignment VALUES", val_lst)

            # TODO: Check for sanitization

            for index in range(len(target_lst) - 1, -1, -1):
                if target_lst[index] in marked_variables:
                    marked_variables.remove(target_lst[index])
                    for vulnerable_var in val_lst[index]:
                        marked_variables.add(vulnerable_var)

        return parameters, [param in marked_variables for param in parameters]
