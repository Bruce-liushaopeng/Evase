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
    elif isinstance(node, ast.Call):
        if node.func.attr == "replace" and len(node.args) == 2 and node.args[0].value == ";" and not node.args[
                                                                                                         1].value == ";":
            return args

        # resolveCall(node)
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
        # for arg in node.args:
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

    return val_lst,0


def collect_vulnerable_vars_5(func_node, assignments, marked_lst, var_type_lst, injection_vars=[]):
    vulnerable = set()  # params
    parameters = get_function_params(func_node)
    print(parameters)
    print(assignments)
    # marked_lst [{a ->{param1, param2}}, {a->{param3}}]    list<Map<string, set>>
    # var_type_lst [{a -> [Integer]},{a -> [class1,class2]}]
    # add parameter types to var_type all permutations
    index = 0
    while index < len(assignments):
        node = assignments[index]
        print(node)
        if isinstance(node, ast.Assign):
            target_lst = get_all_targets(node)  # [a,b,c]
            val_lst, target_type = get_all_target_values(node)
            print("vals----------")
            print(target_lst)
            print(val_lst)
            # [[a,b], [] for Exec(), [a,d] for d.hey(a)], [[], [src:Exec], [int]]
            print("------------ " + str(len(marked_lst)))
            num_possible_marking = len(marked_lst)
            for i in range(len(target_lst)):
                target = target_lst[i]
                for j in range(num_possible_marking):

                    marked_copy = set()
                    for val in val_lst[i]:
                        print(val)
                        if val in parameters:
                            marked_copy.add(val)
                        elif val in marked_lst[j]:
                            marked_copy = marked_copy.union(marked_lst[j][val])

                    marked_lst[j][target] = marked_copy
                    #var_type_lst[j][target] = target_type[j]
            print(marked_lst)

        elif isinstance(node, ast.Return):
            print()
            # if len(injection_vars) == 0:
            #   for val in return:
            #       for vulnerable_param in marked_lst[val]:
            #           vulnerable.add(vulnerable_param)
            # marked_lst.clear(), var_type_lst.clear()
            # break

        elif node == "if" or node == "while" or node == "for":
            print(str(index) + " here------------")
            index, inner_scope_assignments = get_inner_scope_assignments(index, assignments)
            print(str(index)+ " here------------")

            print(inner_scope_assignments)
            prev_marked_lst = copy_list_map_set(marked_lst)
            prev_var_type_lst = copy_list_map_set(var_type_lst)

            for inner_scope_assignment in inner_scope_assignments:
                copy_marked_lst = copy_list_map_set(prev_marked_lst)
                copy_var_type_lst = copy_list_map_set(prev_var_type_lst)

                new_vulnerable = collect_vulnerable_vars_5(func_node, inner_scope_assignment, copy_marked_lst, copy_var_type_lst)
                marked_lst.extend(copy_marked_lst)
                var_type_lst.extend(copy_var_type_lst)
                vulnerable = vulnerable.union(new_vulnerable)
        index += 1

    if len(injection_vars) != 0:
        for val in injection_vars:
            print(val)
            for marked in marked_lst:
                if val not in marked: continue
                print(marked)
                for vulnerable_param in marked[val]:
                    vulnerable.add(vulnerable_param)
    print(vulnerable)
    return vulnerable


def get_inner_scope_assignments(index, assignments):
    stack = []
    stack.append("end" + assignments[index])
    index += 1
    inner_assignments = [[]]
    assignment_ind = 0;

    while len(stack) != 0:
        node = assignments[index]
        if node == "if" or node == "while" or node == "for":
            stack.append("end" + node)
        elif len(stack) == 1 and node == "else":
            inner_assignments.append([])
            assignment_ind += 1
            index += 1
            continue
        elif node == "endif" or node == "endwhile" or node == "endfor":
            removed = stack.pop()
            if removed != node: print("not same val" + removed + " " + node)
            if len(stack) == 0:
                index += 1
                break

        inner_assignments[assignment_ind].append(node)
        index += 1

    return index-1, inner_assignments


def copy_list_map_set(list_map_set):
    copy = []
    for map_set in list_map_set:
        copy.append(map_set.copy())
    return copy

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
        collect_vulnerable_vars_5(func_node, assignment_nodes,[{}], [{}], injection_vars)
        # parameters = get_function_params(func_node)
        # marked_variables = set(injection_vars)
        # for assignment in reversed(assignment_nodes):
        #
        #     target_lst, val_lst = get_all_targets(assignment), get_all_target_values(assignment)
        #     print("Assignment TARGETS", target_lst)
        #     print("Assignment VALUES", val_lst)
        #
        #     # TODO: Check for sanitization
        #     add_set = set()
        #     for index in range(len(target_lst) - 1, -1, -1):
        #         if target_lst[index] in marked_variables:
        #             marked_variables.remove(target_lst[index])
        #             for vulnerable_var in val_lst[index]:
        #                 add_set.add(vulnerable_var)
        #     for add_val in add_set:
        #         marked_variables.add(add_val)
        #
        # return parameters, [param in marked_variables for param in parameters]

    def traversalFromExec(self, assignment_nodes: List[ast.Assign], func_node, injection_vars: Collection[ast.Name]):
        print()
        """
        vulnerableLocations = set()
        visitedFunc = set()
        queue = queue()
        
        queue.add(Node(func_name, assignments, tags, injection_vars)
        
        while not queue.isEmpty():
            node = queue.get()
            if node.get_tags().contains("app.route"):
                #check to parameter and body as func -> add to vulnerable locations In api call.
            else:
                vulnerable_vars = collect_vulnerable_var(node.assignments, node.get_name, node.get_injection_vars)
                
                for location in get_function_uses(node.func_name, node.module):
                    # must be unique based on location_name, location_module, location_assignments, vulnerable_vars
                    
                    if not visitedFunc.contains(location_name, location_module, location_assignments, vulnerable_vars):
                        queue.put(Node(location_name, location_assignments, location_tags, vulnerable_vars))
                        visitedFunc.add(location_name, location_module, location_assignments, vulnerable_vars)
        
        return vulnerableLocations
        
        
        ToDo:   get_function_uses needs to return list [module, function, assignments, tag]
                collect_vulnerable_vars traverse through functions, method to check vulnerability maybe superficially, as getting type is seeming difficult.
                checking assignments but also looking for body function. 
        """
