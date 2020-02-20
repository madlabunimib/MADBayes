import numpy as np
import networkx as nx
from networkx.algorithms.moral import moral_graph
from . import weighted_imputation as wi

def test_moralize():
    # Generate random graphs from nodes count
    nodes = [1, 10, 25, 50, 75, 100, 250, 500]
    graphs = [
        nx.gnp_random_graph(n, 0.5, directed=True)
        for n in nodes
    ]
    # Transform random graphs to DAGs by edge selection
    graphs = [
        nx.DiGraph([(u,v) for (u,v) in G.edges() if u < v])
        for G in graphs
    ]
    # Check if transformed graphs are DAGs
    are_dags = [nx.is_directed_acyclic_graph(G) for G in graphs]
    assert(all(are_dags))
    # Moralize graphs with reference function and extract matrices
    morals = [moral_graph(G) for G in graphs]
    morals = [nx.to_numpy_array(G).astype(bool) for G in morals]
    # Moralize graphs with test function and extract matrices
    wi_graphs = [wi.Graph.from_networkx(G) for G in graphs]
    wi_morals = [wi.moralize(G) for G in wi_graphs]
    wi_morals = [G.get_adjacency_matrix() for G in wi_morals]
    # Check if graphs are equals
    are_equals = [np.array_equal(morals[i], wi_morals[i]) for i in range(len(nodes))]
    assert(all(are_equals))
