import ast

from backend.depanalyze.modulestructure import ModuleAnalysisStruct
from backend.depanalyze.projectstructure import ProjectAnalysisStruct


def get_function_module_uses(func_node: ast.FunctionDef, prj_struct: ProjectAnalysisStruct):
    name = func_node.name
    mdls = []
    for k, v in prj_struct.get_module_structure().items():
        for imp, (imp_mdl, imp_name) in v.get_module_imports():
            if name == imp_name:
                mdls.append(imp_mdl)

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


def get_function_call_origin(func_node: ast.Call, mdl_struct: ModuleAnalysisStruct):
    fn_name = func_node.func.id
    mdls = []
    for imp, (imp_mdl, imp_name) in mdl_struct.get_module_imports():
        if fn_name == imp_name:
            mdls.append(imp_mdl)

    return mdls