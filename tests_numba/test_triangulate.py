import numpy as np
import networkx as nx
from . import madbayes as mb

def test_triangulate():
    # Generate random graphs from nodes count
    nodes = [2, 10, 25, 50, 75, 100]
    graphs = [
        nx.gnp_random_graph(n, 0.5, directed=False)
        for n in nodes
    ]
    wi_graphs = [mb.Graph.from_networkx(G) for G in graphs]
    wi_triang = [mb.triangulate(graph) for graph in wi_graphs]
    wi_triang = [nx.is_chordal(graph.to_networkx()) for graph in wi_triang]
    assert(all(wi_triang))
