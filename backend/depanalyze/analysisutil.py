from typing import Dict, List
import ast
import os
from backend.depanalyze.importresolver import ModuleImportResolver
from backend.depanalyze.surfacedetector import SurfaceLevelVisitor
from modulestructure import ModuleAnalysisStruct


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


if __name__ == '__main__':
    from pprint import pprint

    asts = dir_to_module_structure(r"C:\Users\Anthony\Desktop\Desktop\Proj\parser")
    pprint(asts)
    print("asts")
    get_dependency_relations(r"C:\Users\Anthony\Desktop\Desktop\Proj\parser", asts)
    for x in asts.keys():
        print("key " + x)
        print(asts[x].get_local_imports())
        print(asts[x].get_module_imports())
