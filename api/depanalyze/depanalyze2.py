import pyan
from glob import glob
import os
import networkx as nx


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

    filenames = glob(os.path.join(os.path.dirname(__file__), '..', 'User File/**/*.py'), recursive=True)
    print(filenames)
    v = pyan.CallGraphVisitor(filenames, root=os.path.join(os.path.dirname(__file__), '..', 'User File'))

    # collect and sort defined nodes
    edges = []
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



    print("EDGES")
    print(v.nodes)
    print("DEFINES")
    print(v.defines_edges)
    print("USES")
    print(v.uses_edges)

    dep_tree = {
        
    }

    print(visited_nodes)
    print(edges)

    return visited_nodes, edges

res = get_dependency_relations()
print(res[1])