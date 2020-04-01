import numpy as np
import networkx as nx
from . import weighted_imputation as wi

def test_perfect_numbering():
    # Generate random graphs from nodes count
    nodes = [2, 10, 25, 50]
    graphs = [
        nx.gnp_random_graph(n, 0.5, directed=True)
        for n in nodes
    ]
    # Transform to Wi Graphs
    graphs = [wi.Graph.from_networkx(G) for G in graphs]
    graphs = [wi.triangulate(graph) for graph in graphs]
    numberings = [wi.perfect_numbering(graph) for graph in graphs]
    numberings = [
        [
            set(wi.boundary(graphs[i], numbering[:j])).intersection(set(numbering[:j-1]))
            for j, _ in enumerate(numbering)
        ]
        for i, numbering in enumerate(numberings)
    ]
    numberings = [
        all([
            wi.is_complete(wi.subgraph(graphs[i], list(nodes)))
            for nodes in numbering
        ])
        for i, numbering in enumerate(numberings)
    ]
    assert(all(numberings))
