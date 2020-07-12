import networkx as nx
from . import madbayes as mb


def test_maximal_cilques():
    for nodes in [2, 10, 25, 50]:
        G = nx.gnp_random_graph(nodes, 0.3, directed=False)
        G = nx.Graph([(u, v) for (u, v) in G.edges if u < v])
        g = mb.backend.Graph([
            tuple([str(e) for e in edge]) for edge in G.edges
        ])

        cliques = nx.find_cliques(G)
        cliques = {
            tuple(sorted([str(node) for node in clique]))
            for clique in cliques
        }

        mb_cliques = mb.backend.maximal_cliques(g)
        mb_cliques = {
            tuple(sorted(clique))
            for clique in mb_cliques
        }

        assert(cliques == mb_cliques)
