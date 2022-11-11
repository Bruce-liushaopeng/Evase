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



def make_dependency_graph():

    filenames = glob(os.path.join(os.path.dirname(__file__), "User File/flask_webgoat/**/*.py"), recursive=True)
    v = pyan.CallGraphVisitor(filenames)

    # collect and sort defined nodes
    edges = []
    
    visited_nodes = []
    for name in v.nodes:
        for node in v.nodes[name]:
            if node.defined:
                visited_nodes.append(node)
    visited_nodes.sort(key=lambda x: (x.namespace, x.name))

    for n in v.defines_edges:
        if n.defined:
            for n2 in v.defines_edges[n]:
                if n2.defined:
                    edges.append((n, n2))

    dep_tree = {
        
    }

    print(v.scopes)

    print(visited_nodes)
    print(edges)

    return visited_nodes, edges

res = make_dependency_graph()
print(res[1])