import ast
import os
from _ast import Module, ImportFrom
from pathlib import Path


class ModuleImportResolver(ast.NodeTransformer):
    def __init__(self, surface_values, directory):
        self.directory = directory
        self.is_surface = True
        self.dependencies = {}
        self.surface_values = surface_values

    def get_dependencies(self):
        return self.dependencies

    def set_key(self, key):
        self.key = key

    def visit_Module(self, node: Module):
        super().generic_visit(node)
        self.is_surface = True
        return node

    def visit_Import(self, node: Module):

        for alias_node in node.names:
            name = alias_node.name

            #absolute import path
            if "." in name:
                vals = alias_node.name.split(".")
                name = vals[len(vals)-1]
            #does not have full path
            else:
                vals = self.key.split(".")
                vals[len(vals)-1] = name
                filepath = Path(self.directory+os.sep+os.sep.join(vals)+".py")
                #if it exists in local directory it is a local file, not library
                if filepath.is_file():
                    alias_node.name = ".".join(vals)

            #only will overwrite surface module imports
            if self.is_surface:
                if alias_node.asname is None:
                    self.dependencies[name] = alias_node.name
                else:
                    self.dependencies[alias_node.asname] = alias_node.name

        prev = self.is_surface
        self.is_surface = False
        super().generic_visit(node)
        self.is_surface = prev
        return node

    def visit_ImportFrom(self, node: ImportFrom):
        module_name = node.module
        #absolute path
        if "." in module_name:
            vals = node.module.split(".")
            module_name = vals[len(vals)-1]
        #only local name import
        else:
            vals = self.key.split(".")
            vals[len(vals)-1] = node.module
            filepath = Path(self.directory+os.sep+os.sep.join(vals)+".py")
            #if it exists in local directory it is a local file, not library
            if filepath.is_file():
                node.name = ".".join(vals)

        if node.names[0].name == "*" and "." in node.name:
            surface_level_vals = self.surface_values[node.name]
            lst = []
            for surface_level_val in surface_level_vals:
                lst.append(ast.alias(surface_level_val))
            node.names = lst

        if not self.is_surface:
            super().generic_visit(node)
            return node

        for alias_node in node.names:
            if alias_node.name == "*":
                break
            #only will overwrite surface module imports
            if not hasattr(alias_node, "asname") or alias_node.asname is None:
                self.dependencies[alias_node.name] = [node.name, alias_node.name]
            else:
                self.dependencies[alias_node.asname] = [node.name, alias_node.name]

        prev = self.is_surface
        self.is_surface = False
        super().generic_visit(node)
        self.is_surface = prev
        return node

    def generic_visit(self, node):
        prev = self.is_surface
        self.is_surface = False
        super().generic_visit(node)
        self.is_surface = prev
        return node
