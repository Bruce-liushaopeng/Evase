import json
from typing import List, Dict, Any
import ast

from backend.depanalyze.modulestructure import ModuleAnalysisStruct
from backend.depanalyze.projectstructure import ProjectAnalysisStruct
from backend.sql_injection.injectionutil import get_all_vars
from backend.sql_injection.vulnerabletraversal import VulnerableTraversalChecker


class InjectionNodeVisitor(ast.NodeVisitor):
    def __init__(self, project_struct: ProjectAnalysisStruct, module_key):
        self.execute_funcs = {}
        self.vulnerable_funcs = {}
        self.current_func_node = None
        self.lst_of_assignments = []
        self.sql_marker = VulnerableTraversalChecker()
        self.if_flag = True
        self.project_struct = project_struct
        self.module_key = module_key

        self.sql_import_name = []
        self.found_cursors = []
        self.found_execute_cursors = {}

        mod_strct = project_struct.get_module_structure()
        for index in mod_strct.keys():
            item = mod_strct.get(index)
            self.check_imports(item)

    def check_imports(self, module_strct: ModuleAnalysisStruct):
        print("--- Got module struct ---")
        # f = open('sql_imports.json')
        # data = json.load(f)
        sql_imports = ["sqlite3", "mysql", "postgresql", "pyscopg2"]
        module_imports = module_strct.get_module_imports()

        for sample_import in module_imports.keys():
            module_imp_value = module_imports.get(sample_import)
            if module_imp_value[0] in sql_imports and sample_import not in self.sql_import_name:
                self.sql_import_name.append(sample_import)

        local_imports = module_strct.get_local_imports()
        for sample_local in local_imports.keys():
            local_imp_value = local_imports.get(sample_local)
            if local_imp_value[0] in sql_imports and sample_local not in self.sql_import_name:
                self.sql_import_name.append(sample_local)

        # print("Module imports ("+index+"): ")
        # print(item.get_module_imports())
        # print("Local imports ("+index+": ")
        # print(item.get_local_imports())
        print("--- Done ---")
        # Check imports from file and add to sql_import_names

        # for sql_name in data['sql_imports']:
        #     print('Found sql package name: '+sql_name)

    def check_cursor(self, node: ast.Call) -> bool:
        call_func = node.func
        if isinstance(call_func, ast.Attribute):   # This may need to be double checked for ast.Attribute
            func_attr = call_func.attr

            if func_attr.lower() == 'cursor':
                attr_name_node = call_func.value
                return isinstance(attr_name_node, ast.Name) and any(
                    attr_name_node.id == sql_import for sql_import in self.sql_import_name)

    def handle_cursor(self, targs: list[ast.expr], call_node: ast.Call):
        for targ in targs:
            if isinstance(targ, ast.Name) and isinstance(targ.ctx, ast.Store):
                cursor_obj_name = targ.id
                for saved_execute_cursor in self.found_execute_cursors.keys():
                    if saved_execute_cursor == cursor_obj_name:
                        print(self.lst_of_assignments)
                        self.visit_execute(call_node)
                        super().generic_visit(call_node)

                        return   # Not sure about this
                self.found_cursors.append(cursor_obj_name)

    def get_execute_funcs(self) -> dict[Any, Any]:
        return self.execute_funcs

    def visit_Expr(self, node: ast.Expr):
        super().generic_visit(node)

    def visit_Assign(self, node: ast.Assign):

        node_value = node.value
        if isinstance(node_value, ast.Call):
            valid_cursor = self.check_cursor(node_value)
            if valid_cursor:
                node_targets = node.targets
                self.handle_cursor(node_targets, node_value)

        print(ast.dump(node))
        self.lst_of_assignments.append(node)
        super().generic_visit(node)

    def visit_If(self, node: ast.If):
        if self.if_flag:
            self.lst_of_assignments.append("if")
        for val in node.body:
            self.visit(val)

        if len(node.orelse) > 0:
            prev = self.if_flag
            self.if_flag = False
            self.else_visit(node.orelse)
            self.if_flag = prev

        if self.if_flag:
            self.lst_of_assignments.append("endif")

    def else_visit(self, nodes):
        if len(nodes) == 0:
            self.lst_of_assignments.append("endelse")
        else:
            self.lst_of_assignments.append("else")
            for node in nodes:
                self.visit(node)

    def visit_While(self, node: ast.While) -> Any:
        self.lst_of_assignments.append("while")
        super().generic_visit(node)
        self.lst_of_assignments.append("endwhile")

    def visit_For(self, node: ast.For) -> Any:
        self.lst_of_assignments.append("for")
        super().generic_visit(node)
        self.lst_of_assignments.append("endfor")

    def visit_Return(self, node: ast.Return) -> Any:
        self.lst_of_assignments.append(node)
        super().generic_visit(node)

    def visit_Call(self, node: ast.Call):
        if hasattr(node.func, "attr") and node.func.attr == "execute":
            func_node = node.func
            if isinstance(func_node, ast.Attribute) and isinstance(func_node.value, ast.Name):
                name_node = func_node.value
                execute_cursor = name_node.id
                for saved_cursor in self.found_cursors:
                    if saved_cursor == execute_cursor:
                        self.found_cursors.remove(saved_cursor)

                        print(self.lst_of_assignments)
                        self.visit_execute(node)
                        super().generic_visit(node)

                        return   # Not sure about this

                # self.found_execute_cursors.append(execute_cursor)
                self.found_execute_cursors[execute_cursor] = [self.lst_of_assignments.copy(), self.current_func_node, get_all_vars(node.args[0]), self.project_struct, self.module_key]

    def visit_execute(self, node: ast.Call):
        lst = self.lst_of_assignments.copy()

        print(self.lst_of_assignments)

        arg_list = get_all_vars(node.args[0])
        curr_scope = self.get_current_scope()
        print("EXEC found, curr scope:", curr_scope)
        print(self.current_func_node.parent_classes)

        result = self.sql_marker.traversal_from_exec(lst, self.current_func_node, arg_list, self.project_struct,
                                                     self.module_key)
        if len(result) > 0:
            module_full_name = f'{self.module_key}.{self.current_func_node.name}'
            self.vulnerable_funcs[module_full_name] = result
        self.execute_funcs[curr_scope] = self.current_func_node

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self.current_func_node = node
        self.lst_of_assignments = []
        super().generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        self.visit_FunctionDef(node)

    def get_current_scope(self):
        if self.current_func_node:
            return self.current_func_node.name
        else:
            return ""

    def get_vulnerable_funcs(self):
        return self.vulnerable_funcs


if __name__ == '__main__':
    anyone = InjectionNodeVisitor()
