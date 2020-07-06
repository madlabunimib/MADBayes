import numpy as np
import networkx as nx
from networkx.algorithms.moral import moral_graph
from . import madbayes as mb

def test_maximal_cilques():
    # Generate random graphs from nodes count
    nodes = [2, 10, 25, 50, 75, 100, 250]
    graphs = [
        nx.gnp_random_graph(n, 0.3, directed=False)
        for n in nodes
    ]
    # Find all maximal cliques with reference function
    cliques = [nx.find_cliques(G) for G in graphs]
    # Transform lists of node indices in sets of node labels
    cliques = [
        set([
            tuple(sorted([str(node) for node in nodes]))
            for nodes in clique
        ])
        for clique in cliques
    ]
    # Find all maximal cliques with test function
    wi_graphs = [mb.Graph.from_networkx(G) for G in graphs]
    wi_cliques = [mb.maximal_cliques(graph) for graph in wi_graphs]
    wi_cliques = [
        set([tuple(sorted(nodes)) for nodes in clique])
        for clique in wi_cliques]
    # Check if graphs have the same maximal cliques
    are_equals = [cliques[i] == wi_cliques[i] for i in range(len(nodes))]
    assert(all(are_equals))
