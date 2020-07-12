import networkx as nx
from . import madbayes as mb


def test_chordal():
    for nodes in [10, 25, 50, 100]:
        G = nx.gnp_random_graph(nodes, 0.5, directed=True)
        G = nx.DiGraph([(u, v) for (u, v) in G.edges if u < v])
        g = mb.backend.DirectedGraph([
            tuple([str(e) for e in edge]) for edge in G.edges
        ])
        g = mb.backend.chordal(g)
        assert(g.is_chordal())
