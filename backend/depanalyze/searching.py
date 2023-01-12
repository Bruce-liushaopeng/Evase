import ast

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


def get_function_call_origin(func_node: ast.Call, mdl_struct: ModuleAnalysisStruct, prj_struct: ProjectAnalysisStruct,
                             caller_type: str = None):
    fn_name = func_node.func.id

    if caller_type is None:
        print("Regular function call, not an object function call.")
    else:
        fn_name = caller_type + '.' + fn_name

    # using the dependencies of the current module, find the modules that is uses the function from (should be one).
    mdls = []
    for imp, (imp_mdl, imp_name) in mdl_struct.get_module_imports().items():
        if fn_name == imp_name:
            mdls.append(imp_mdl)

    # after finding the module(s) that this function comes from, visit them.
    fn_defs = []
    for mdl in mdls:
        mdl = prj_struct.get_module(mdl)
        for mdl_func in mdl.get_funcs():
            if mdl_func.name == fn_name:
                fn_defs.append(mdl_func)

    return fn_defs
