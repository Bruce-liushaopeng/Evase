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

    def collect_vulnerable_vars(self, func_node, assignments, possible_marked_var_to_params, var_type_lst, injection_vars=[]):
        vulnerable = set()  # params
        parameters = get_function_params(func_node)
        print(parameters)
        print(assignments)
        #               possible flow         possible flow
        # marked_lst [{a ->{param1, param2}}, {a->{param3}}]      list<Map<string, set>>
        # var_type_lst [{a -> [Integer]},{a -> [class1,class2]}]

        index = 0
        while index < len(assignments):
            node = assignments[index]

            if isinstance(node, ast.Assign):
                # variables being assigned a value
                target_lst = get_all_targets(node)
                # values of variables being assigned
                val_lst, target_type = get_all_target_values(node)

                print("----------")
                print(target_lst)
                print(val_lst)
                print("----------")

                for i in range(len(target_lst)): # for each variable being assigned
                    target_variable = target_lst[i]

                    for j in range(len(possible_marked_var_to_params)): # update all possible marked variables to params, for target_variable
                        marked_new = set()
                        for val in val_lst[i]: # values of variables being assigned to corresponding target_variable
                            if val in parameters:
                                marked_new.add(val)
                            # get parameters that val is equal to and add to marked_new
                            elif val in possible_marked_var_to_params[j]:
                                marked_new = marked_new.union(possible_marked_var_to_params[j][val])

                        possible_marked_var_to_params[j][target_variable] = marked_new
                        #var_type_lst[j][target] = target_type[j]
                print(possible_marked_var_to_params)

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
                prev_marked_lst = copy_list_map_set(possible_marked_var_to_params)
                prev_var_type_lst = copy_list_map_set(var_type_lst)

                for inner_scope_assignment in inner_scope_assignments:
                    copy_marked_lst = copy_list_map_set(prev_marked_lst)
                    copy_var_type_lst = copy_list_map_set(prev_var_type_lst)

                    # determine marked_lst in inner function, new_vulnerable is for when function returns are being analyzed
                    new_vulnerable = self.collect_vulnerable_vars(func_node, inner_scope_assignment, copy_marked_lst, copy_var_type_lst)

                    # add inner scope marked_lst to previous possible_marked_var_to_params
                    possible_marked_var_to_params.extend(copy_marked_lst)
                    var_type_lst.extend(copy_var_type_lst)
                    vulnerable = vulnerable.union(new_vulnerable)
            index += 1

        # if injection_vars -> cursor.execute() determine if vars used in injection are dangerous
        if len(injection_vars) != 0:
            for val in injection_vars:
                for marked in possible_marked_var_to_params:
                    if val not in marked: continue
                    print(marked)
                    for vulnerable_param in marked[val]:
                        vulnerable.add(vulnerable_param)
        print(vulnerable)
        return vulnerable

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
