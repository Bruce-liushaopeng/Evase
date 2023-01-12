import ast
import os
from pathlib import Path
from typing import Dict

from backend.depanalyze.importresolver import ModuleImportResolver
from backend.depanalyze.modulestructure import ModuleAnalysisStruct
from backend.depanalyze.scoperesolver import ScopeResolver
from backend.depanalyze.surfacedetector import SurfaceLevelVisitor


def resolve_project_imports(dirpath: str, module_mapping: Dict[str, ModuleAnalysisStruct]):
    """
    Define the dependencies between modules.

    :param module_mapping: The mapping of module names to their analysis structures
    :param dirpath: The path to the directory of the project
    :return: An altered module mapping containing
    """

    surface_values = {}
    for module_key in module_mapping.keys():
        ast_tree = module_mapping[module_key].get_ast()
        surface_detector = SurfaceLevelVisitor()
        surface_detector.visit(ast_tree)
        surface_values[module_key] = surface_detector.get_surface_names()

    for module_key in module_mapping.keys():
        import_resolver = ModuleImportResolver(surface_values, dirpath)
        import_resolver.set_key(module_key)
        ast_tree = module_mapping[module_key].get_ast()
        modified_ast = import_resolver.visit(ast_tree)
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


class ProjectAnalysisStruct:

    def __init__(self, prj_name: str, prj_root: str):
        """
        Constructor for instances of project analysis structure.

        :param prj_name: The name of the project
        :param prj_root: The root directory of the project
        """
        self.prj_name = prj_name

        if not os.path.exists(prj_root):
            raise ValueError("Can't accept a file path that doesn't exist.")

        self._prj_root = prj_root
        self._module_structure = dir_to_module_structure(self._prj_root)
        self.resolve_scopes(ScopeResolver())
        resolve_project_imports(self._prj_root, self._module_structure)

    def resolve_module_funcs(self):
        for mdl in self._module_structure.values():
            mdl.resolve_funcs()

    def resolve_scopes(self, scr: ScopeResolver):
        for mdl in self._module_structure.values():
            mdl.resolve_scopes(scr)
            scr.reset()

    def get_prj_root(self):
        """
        Retrieve the root given for the project.

        :return: The root of the project
        """
        return self._prj_root

    def get_module_structure(self) -> Dict[str, ModuleAnalysisStruct]:
        """
        Retrieve the structure of the modules (use after processing)

        :return: Mapping of module names to analysis structures
        """
        return self._module_structure

    def get_module(self, module_key) -> ModuleAnalysisStruct:
        """
        Retrieve the structure of the module

        :return: module analysis structures
        """
        return self._module_structure.get(module_key)
