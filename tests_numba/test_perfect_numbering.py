import numpy as np
import networkx as nx
from . import madbayes as mb

def test_perfect_numbering():
    # Generate random graphs from nodes count
    nodes = [3, 10, 25, 50]
    graphs = [
        nx.gnp_random_graph(n, 0.5, directed=True)
        for n in nodes
    ]
    # Transform to Wi Graphs
    graphs = [mb.Graph.from_networkx(G) for G in graphs]
    graphs = [mb.triangulate(graph) for graph in graphs]
    numberings = [mb.perfect_numbering(graph) for graph in graphs]
    numberings = [
        [
            set(mb.boundary(graphs[i], numbering[:j])).intersection(set(numbering[:j-1]))
            for j, _ in enumerate(numbering)
        ]
        for i, numbering in enumerate(numberings)
    ]
    numberings = [
        all([
            mb.is_complete(mb.subgraph(graphs[i], list(nodes)))
            for nodes in numbering
        ])
        for i, numbering in enumerate(numberings)
    ]
    assert(all(numberings))
