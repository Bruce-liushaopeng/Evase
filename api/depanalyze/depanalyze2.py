import ast

import pyan
from glob import glob
import os

from api.injection import InjectionDetectionVisitor
from file_struct import FileStruct


class DependencyTree:

    def __init__(self):
        self.nodes = {}
        self.edges = {}


class Module:

    def __init__(self):
        self.props = {}


class Node:
    def __init__(self):
        self.props = {}


def make_dependency_graph(nodes: list, edges: list):
    dct = {
        "u"
    }


def get_dependency_relations():
    filenames = glob(os.path.join(os.path.dirname(__file__), 'src/**/*.py'), recursive=True)
    v = pyan.CallGraphVisitor(filenames)

    # collect and sort defined nodes
    edges = []
    uses_edges = []
    visited_nodes = []
    for name in v.nodes:
        for node in v.nodes[name]:
            if node.defined:
                visited_nodes.append(node)

    for n in v.defines_edges:
        if n.defined:
            for n2 in v.defines_edges[n]:
                if n2.defined:
                    edges.append((n, n2))

    for n in v.uses_edges:
        if n.defined:
            for n2 in v.uses_edges[n]:
                if n2.defined:
                    uses_edges.append((n, n2))

    print("EDGES")
    print(v.nodes)
    print("DEFINES")
    print(v.defines_edges)
    print("USES")
    print(v.uses_edges)

    dep_tree = {

    }
    print("next")
    #print(visited_nodes)
    #print(edges)

    return [visited_nodes, v, v.uses_edges]


def iter(dir, id, asts):
    with os.scandir(dir) as it:
        for entry in it:
            if entry.is_dir():
                iter(dir + "/" + entry.name, id + "." + entry.name, asts)

            elif entry.name.endswith('.py') and entry.is_file():
                name = entry.name[:len(entry.name) - 3]
                print(entry.name + " " + id + "." + name + " "+dir + "/" + entry.name)
                f = open(dir + "/" + entry.name, "r")
                ast_file = ast.parse(f.read())
                asts[id + "." + name] = FileStruct(ast_file)
                f.close()


asts = dict()

print(os.path.dirname(__file__))
iter(os.path.dirname(__file__) + "/src", "api.depanalyze.src", asts)

res = get_dependency_relations()
print(res[2])
for node in res[2]:
    if node.defined:
        node_name = node.__str__()
        if "<Node module" in node_name:
            file_name = node_name.split("<Node module:")[1]
            file_name = file_name[: len(file_name)-1]

        elif "<Node function" in node_name:
            file_name = node_name.split("<Node function:")[1]
        elif "<Node class" in node_name:
            file_name = node_name.split("<Node class:")[1]
        elif "<Node method" in node_name:
            file_name = node_name.split("<Node method:")[1]
        print(file_name)
        print(res[2].get(node))

for x in asts.keys():
    print(x)
    detector = InjectionDetectionVisitor()
    print(asts.get(x).get_ast())
# print(res[1])
