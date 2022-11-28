from typing import List, Collection
import ast


def get_function_params(node: ast.AST) -> set:
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


def collect_all_vars(node: ast.AST) -> set:
    """
    Recursively looks at a node and collects the variables used in that node.

    :param node: The node to look through
    :return: The set of variable ids used inside a node
    """

    args = set()

    if hasattr(node, "id"):
        print("variable")
        print(node.__dict__)
        args.add(node.id)
    elif hasattr(node, "elts"):
        print("list-like")
        print(node.__dict__)
        for subarg in node.elts:
            for subsubarg in collect_all_vars(subarg):
                args.add(subsubarg)
    elif isinstance(node, ast.Dict):
        print("dict")
        print(node.__dict__)
        for subarg in node.values:
            for subsubarg in collect_all_vars(subarg):
                args.add(subsubarg)
    elif isinstance(node, ast.BinOp):
        for l_subarg in collect_all_vars(node.left):
            args.add(l_subarg)
        for r_subarg in collect_all_vars(node.right):
            args.add(r_subarg)

    elif hasattr(node, "args"):
        print("function call")
        print(node.__dict__)
        for arg in node.args:
            for subarg in collect_all_vars(arg):
                args.add(subarg)

    elif hasattr(node, "value"):
        print("value?")
        print(node.__dict__)
        for subarg in collect_all_vars(node.value):
            args.add(subarg)

    return args


def quicktest():
    tst = ast.parse("password, b, c = a+c, c, '2'")
    for nod in ast.walk(tst):
        if isinstance(nod, ast.Assign):
            print(collect_all_vars(nod))


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

            target_lst = []  # list of targets for this assignment

            for target in assignment.targets:

                if isinstance(target, ast.Name):
                    target_lst.append(target.id)

                elif hasattr(target, "elts"):
                    for val in target.elts:
                        if hasattr(val, "id"):
                            target_lst.append(val.id)

            print("Assignment TARGETS", target_lst)

            val_lst = collect_all_vars(assignment.value)  # collect all variables mention

            print("Assignment VALUES", val_lst)

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

