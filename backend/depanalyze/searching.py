import ast

from backend.depanalyze.functioncallfinder import FunctionCallFinder
from backend.depanalyze.modulestructure import ModuleAnalysisStruct
from backend.depanalyze.projectstructure import ProjectAnalysisStruct


def get_function_module_uses(func_node: ast.FunctionDef, prj_struct: ProjectAnalysisStruct):
    name = func_node.name
    mdls = []

    # check project structure for any modules that import this function
    for k, v in prj_struct.get_module_structure().items():
        for imp, (imp_mdl, imp_name) in v.get_module_imports():
            if name == imp_name:
                mdls.append(imp_mdl)

    # for each module that uses this function, retrieve the functions that use this function
    funcs = []
    for mdl in mdls:
        fns = []
        mdl_struct = prj_struct.get_module(mdl)
        for fn in mdl_struct.get_funcs():
            for node in ast.walk(fn):
                if isinstance(node, ast.Call):
                    if name == node.func.id:
                        fns.append(fn)
                        break
        funcs.append(fns)

    return mdls, funcs


def get_function_call_origin(func_node: ast.Call, mdl_struct: ModuleAnalysisStruct, prj_struct: ProjectAnalysisStruct, caller_type: str = None):

    if caller_type is None:
        print("Regular function call, not an object function call.")

    fn_name = func_node.func.id
    mdls = []

    # given a function node, find the module it comes from with the dependency graph in ModuleAnalysisStruct
    for imp, (imp_mdl, imp_name) in mdl_struct.get_module_imports():
        if fn_name == imp_name:
            mdls.append(imp_mdl)

    return mdls

def get_function_uses(projectStruc, func_name: str, module_name: str):
    new_found_vulnerable = []
    for key in projectStruc:
        module_struct = projectStruc[key]
        case, asname = 0, None
        if not key == module_name:
            case, asname = differentiate_imports(module_struct, func_name, module_name)
        else:
            case = 2

        # for each case, run a node vistor, and tell the node vistor what to look for thru parameter
        # reference sql injection algo development notion, page api.py(for test vul func calls) for more information of the four cases.
        print(f'----   scaning vulnerable usages in {module_struct.get_name()} ----')
        func_target = func_name
        module_target = module_name
        if case == 0:
            print(f"CASE 0: no vulnerable usage found")
            continue

        # No modification needed for case 1

        elif case == 2:
            print(f"CASE 2: vulnerable function found imported, next step look for function calls [{func_name}]")
            module_target = None
        elif case == 3:
            print(f"CASE 3: vulnerable function found imported using AS, next step look for function calls [{asname}]")
            module_target = None
            func_target = asname

        elif case == 4:
            print(f"CASE 4: vulnerable class found imported using AS, next step look for [{asname}.{func_name}]")
            module_target = asname

        call_finder = FunctionCallFinder(module_target, func_target)
        call_finder.visit(module_struct.ast_tree)
        for func in call_finder.foundCallingDict:
            print("new vulnerable function : " + func)
            print("new vulnerable module : " + key)
            print(f"ast node {str(call_finder.foundCallingDict[func])}")

def differentiate_imports(moduleStructure: ModuleAnalysisStruct, vul_func: str, vul_module_name: str):
    # function can tell us if the vulnerale is imported as function or module
    localImport = moduleStructure.get_local_imports()
    moduleImport = moduleStructure.get_module_imports()
    # case1, importing entire module
    if (vul_module_name in localImport.keys() or vul_module_name in moduleImport.keys()):
        return (1, vul_module_name)

    # case2, importing vulnerable function
    print(moduleImport.keys())

    if (vul_func in localImport.keys() or vul_func in moduleImport.keys()):
        return (2, vul_func)

    # case3, importing vul function with AS
    for key in localImport:
        func_as_name = key
        className, originalFuncName = localImport[key]
        if originalFuncName == vul_func:
            return (3, func_as_name)

    for key in moduleImport:
        func_as_name = key
        className, originalFuncName = moduleImport[key]
        if originalFuncName == vul_func:
            return (3, func_as_name)

    # case4, importing entire module with AS
    for key in localImport:
        className, class_as_Name = localImport[key]
        if className == vul_module_name:
            return (4, class_as_Name)

    for key in moduleImport:
        className, class_as_Name = moduleImport[key]
        if className == vul_module_name:
            return (4, class_as_Name)

    # not found related import, this file is not related for this vul
    return (0, None)
