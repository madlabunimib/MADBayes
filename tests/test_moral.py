import networkx as nx
from networkx.algorithms.moral import moral_graph as moral
from . import madbayes as mb

def test_moralize():
    for nodes in [2, 10, 25, 50]:
        G = nx.gnp_random_graph(nodes, 0.5, directed=True)
        G = nx.DiGraph([(u, v) for (u, v) in G.edges if u < v])
        g = mb.DirectedGraph([
            tuple([str(e) for e in edge]) for edge in G.edges
        ])

        G = moral(G)
        g = mb.moral(g)

        edges = [tuple(sorted([str(e) for e in edge])) for edge in G.edges]
        assert(sorted(edges) == sorted(g.edges))
