import numpy as np
import networkx as nx
from . import weighted_imputation as wi

def test_undirected_graph():
    nodes = [1, 10, 25, 50, 75, 100, 250]
    graphs = [
        nx.gnp_random_graph(n, 0.3, directed=False)
        for n in nodes
    ]
    neighbors = [[list(G.neighbors(node)) for node in G.nodes] for G in graphs]
    boundaries = [list(nx.algorithms.node_boundary(G, list(G.nodes)[0:5])) for G in graphs]
    boundaries = [sorted(boundary) for boundary in boundaries]
    wi_graphs = [wi.Graph.from_networkx(G) for G in graphs]
    wi_neighbors = [[[int(n) for n in graph.neighbors(node)] for node in graph.get_nodes()] for graph in wi_graphs]
    wi_boundaries = [[int(n) for n in graph.boundary(np.array(graph.get_nodes()[0:5]))] for graph in wi_graphs]
    assert(neighbors == wi_neighbors)
    assert(boundaries == wi_boundaries)

def test_directed_graph():
    pass