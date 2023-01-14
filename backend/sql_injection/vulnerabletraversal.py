from typing import Collection, List
import ast
from collections import deque

from backend.sql_injection.node import Node
import backend.depanalyze.searching as searching
import backend.sql_injection.injectionutil as injectionutil


def copy_list_map_set(list_map_set):
    copy = []
    for map_set in list_map_set:
        copy.append(map_set.copy())
    return copy


class VulnerableTraversalChecker:
    def traversal_from_exec(self, assignments: List[ast.Assign], func_node, injection_vars: Collection[ast.Name],
                          project_struct, module):

        vulnerable_locations = set()
        visited_func = set()
        queue = deque()
        modules = project_struct.get_module_structure()
        queue.append(Node(func_node, assignments, injection_vars, module))

        print(injection_vars)
        print("start of bfs")
        while len(queue) != 0:
            node = queue.popleft()
            # if node.get_tags().contains("app.route"):
            # check to parameter and body as func -> add to vulnerable locations In api call.
            # else:
            vulnerable_vars = self.collect_vulnerable_vars(node.get_func_node(), node.get_assignments(), [{}], [{}],  node.get_injection_vars())
            for location in searching.get_function_uses(modules, 'adminExec', 'find_uses_tests.sql_injection_vul5'):
                print("vulnerable asdf")
                print(location)
                # must be unique based on location_name, location_module, location_assignments, vulnerable_vars

                # if not visitedFunc.contains(location_name, location_module, location_assignments, vulnerable_vars):
                #     queue.put(Node(location_name, location_assignments, location_tags, vulnerable_vars))
                #     visitedFunc.add(location_name, location_module, location_assignments, vulnerable_vars)

        return vulnerable_locations


    def collect_vulnerable_vars(self, func_node, assignments, possible_marked_var_to_params, var_type_lst,
                                injection_vars={}):
        vulnerable = set()  # params
        parameters = injectionutil.get_function_params(func_node)
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
                target_lst = injectionutil.get_all_targets(node)
                # values of variables being assigned
                val_lst, target_type = injectionutil.get_all_target_values(node)

                # print("----------")
                # print(target_lst)
                # print(val_lst)
                # print("----------")

                for i in range(len(target_lst)):  # for each variable being assigned
                    target_variable = target_lst[i]

                    for j in range(
                            len(possible_marked_var_to_params)):  # update all possible marked variables to params, for target_variable
                        marked_new = set()
                        for val in val_lst[i]:  # values of variables being assigned to corresponding target_variable
                            if val in parameters:
                                marked_new.add(val)
                            # get parameters that val is equal to and add to marked_new
                            elif val in possible_marked_var_to_params[j]:
                                marked_new = marked_new.union(possible_marked_var_to_params[j][val])

                        possible_marked_var_to_params[j][target_variable] = marked_new
                        # var_type_lst[j][target] = target_type[j]
                # print(possible_marked_var_to_params)

            elif isinstance(node, ast.Return):
                print()
                # if len(injection_vars) == 0:
                #   for val in return:
                #       for vulnerable_param in marked_lst[val]:
                #           vulnerable.add(vulnerable_param)
                # marked_lst.clear(), var_type_lst.clear()
                # break

            elif node == "if" or node == "while" or node == "for":
                index, inner_scope_assignments = injectionutil.get_inner_scope_assignments(index, assignments)
                prev_marked_lst = copy_list_map_set(possible_marked_var_to_params)
                prev_var_type_lst = copy_list_map_set(var_type_lst)

                for inner_scope_assignment in inner_scope_assignments:
                    copy_marked_lst = copy_list_map_set(prev_marked_lst)
                    copy_var_type_lst = copy_list_map_set(prev_var_type_lst)

                    # determine marked_lst in inner function, new_vulnerable is for when function returns are being analyzed
                    new_vulnerable = self.collect_vulnerable_vars(func_node, inner_scope_assignment, copy_marked_lst,
                                                                  copy_var_type_lst)

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
                    for vulnerable_param in marked[val]:
                        vulnerable.add(vulnerable_param)
        print(vulnerable)
        return vulnerable
