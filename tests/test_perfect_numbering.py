import numpy as np
import networkx as nx
from . import madbayes as mb


def test_perfect_numbering():
    for nodes in [10, 25, 50, 100]:
        g = mb.backend.Graph.random(nodes, 0.5)
        g = mb.backend.chordal(g)
        numbering = mb.backend.maximum_cardinality_search(g)
        # A numbering is perfect iff the subset of nodes derived
        # from boundary(alpha[i]) \cap {alpha[1], ..., alpha[i-1]}
        # identify a complete graph.
        for i, node in enumerate(numbering, start=1):
            subgraph = set(g.neighbors(node)).intersection(set(numbering[:i]))
            subgraph = g.subgraph(list(subgraph))
            assert(subgraph.is_complete())
