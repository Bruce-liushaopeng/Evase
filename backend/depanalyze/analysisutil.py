from typing import Dict, List
import ast
import os
from importresolver import ModuleImportResolver
from surfacedetector import SurfaceLevelVisitor
from modulestructure import ModuleAnalysisStruct
from functioncallfinder import FunctionCallFinder


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
        import_resolver = ModuleImportResolver(surface_values,dirpath)
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

    namesp = dirpath
    if "__init__.py" in os.listdir(dirpath):  # check if the start path itself is a package
        namesp = os.sep.join(dirpath.split(os.sep)[:-1])

    for root, dirs, files in os.walk(dirpath):
        for f in files:
            fullpath = os.path.join(root, f)
            filename, ext = os.path.splitext(fullpath)
            if ext == ".py":
                module_style = filename.replace(namesp + os.sep, '').replace(os.sep, '.')

                with open(fullpath, "r") as fr:
                    tree[module_style] = ModuleAnalysisStruct(module_style, ast.parse(fr.read()))

    return tree

def get_function_uses(projectStruc, func_name: str, module_name: str):
    potentialUsage = []
    for key in projectStruc:
        module_struct = projectStruc[key]
        case, asname = 0, None
        if not key == module_name:
            case, asname = differentiate_imports(module_struct, func_name, module_name)

        # for each case, run a node vistor, and tell the node vistor what to look for thru parameter
        # reference sql injection algo development notion, page api.py(for test vul func calls) for more information of the four cases.
        print(f'----   scaning vulnerable usages in {module_struct.get_name()} ----')
        func_target = func_name
        module_target = module_name
        if case == 0:
            print(f"CASE 0: no vulnerable usage found" )
            continue

        # No modification needed for case 1

        elif case == 2:
            print(f"CASE 2: vulnerable function found imported, next step look for function calls [{func_name}]" )
            module_target = None
        elif case == 3:
            print(f"CASE 3: vulnerable function found imported using AS, next step look for function calls [{asname}]" )
            module_target = None
            func_target = asname

        elif case == 4:
            print(f"CASE 4: vulnerable class found imported using AS, next step look for [{asname}.{func_name}]" )
            module_target = asname
        
        call_finder = FunctionCallFinder(module_target, func_target)
        call_finder.visit(module_struct.ast_tree)
        print(f"function call at line {call_finder.linoFunctionCall} of module \"{module_struct.module_name}\"" )
        print(f"called inside of function: {call_finder.parentFuncScope}")



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
    asts = dir_to_module_structure(bruce_test_path1)
    pprint(asts)
    print("asts")
    get_dependency_relations(bruce_test_path1, asts)
    for x in asts.keys():
        print("=======")
        print("key " + x)
        print(asts[x].get_local_imports())
        print(asts[x].get_module_imports())
