from pathlib import Path
from typing import Dict, List
import ast
import os
from backend.depanalyze.importresolver import ModuleImportResolver
from backend.depanalyze.surfacedetector import SurfaceLevelVisitor
from backend.depanalyze.modulestructure import ModuleAnalysisStruct
from backend.depanalyze.functioncallfinder import FunctionCallFinder


def get_dependency_relations(dirpath: str, module_mapping: Dict[str, ModuleAnalysisStruct]) -> Dict[str, List[str]]:
    """
    Using Pyan3 to convert a directory into a dependency/call graph.

    :param dirpath: The path to the directory
    :return: The mapping of use edges
    """

    surface_values = {}
    for module_key in module_mapping.keys():
        ast = module_mapping[module_key].get_ast()
        surface_detector = SurfaceLevelVisitor()
        surface_detector.visit(ast)
        surface_values[module_key] = surface_detector.get_surface_names()

    for module_key in module_mapping.keys():
        import_resolver = ModuleImportResolver(surface_values, dirpath)
        import_resolver.set_key(module_key)
        ast = module_mapping[module_key].get_ast()
        modified_ast = import_resolver.visit(ast)
        module_mapping[module_key].set_ast(modified_ast)

        module_imports, local_imports = import_resolver.get_dependencies()
        module_mapping[module_key].set_module_imports(module_imports)
        module_mapping[module_key].set_local_imports(local_imports)


def dir_to_module_structure(dirpath: str) -> Dict[str, ModuleAnalysisStruct]:
    """
    Converts a directory into a mapping of package style names to module analysis structures

    :param dirpath: The path to the directory of the code
    :return: A mapping of module names to analysis structures
    """

    tree = {}
    dirpath = Path(dirpath)

    keep_last = any(p.name == "__init__.py" for p in Path.iterdir(dirpath))
    print(keep_last)

    files = dirpath.glob('**/*.py')
    for file in files:
        if keep_last:
            module_style = Path(os.path.splitext(file.relative_to(dirpath.parent))[0])
        else:
            module_style = Path(os.path.splitext(file.relative_to(dirpath))[0])
        module_style = str(module_style).replace(os.sep, '.')

        with open(file, 'r') as openfile:
            tree[module_style] = ModuleAnalysisStruct(module_style, ast.parse(openfile.read()))

    return tree


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


if __name__ == '__main__':
    from pprint import pprint

    anthony_test_path = r"C:\Users\Anthony\Desktop\Desktop\Proj\parser"
    bruce_test_path = r"D:\work\programming\Evase\examples\parser\parser"
    bruce_test_path1 = r"D:\work\programming\Evase\examples\FindVulFuncUsageTest"
    asts = dir_to_module_structure(anthony_test_path)
    pprint(asts)
    print("asts")
    get_dependency_relations(anthony_test_path, asts)
    for x in asts.keys():
        print("=======")
        print("key " + x)
        print(ast.dump(asts[x].get_ast(), indent=2))
