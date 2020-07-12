import networkx as nx
from . import madbayes as mb


def test_undirected_graph():
    for nodes in [2, 10, 25, 50, 75, 100, 250]:
        G = nx.gnp_random_graph(nodes, 0.3, directed=False)
        g = mb.backend.Graph([
            tuple([str(e) for e in edge]) for edge in G.edges
        ])
        for node in g.nodes:
            neighbors = map(lambda x: str(x), G.neighbors(int(node)))
            assert(sorted(neighbors) == sorted(g.neighbors(node)))
        boundary = map(lambda x: str(
            x), nx.algorithms.node_boundary(G, G.nodes))
        assert(sorted(boundary) == sorted(g.boundary(g.nodes)))


def test_directed_graph():
    for nodes in [2, 10, 25, 50]:
        G = nx.gnp_random_graph(nodes, 0.3, directed=False)
        G = nx.DiGraph([(u, v) for (u, v) in G.edges if u < v])
        g = mb.backend.DirectedGraph([
            tuple([str(e) for e in edge]) for edge in G.edges
        ])
        for node in g.nodes:
            parents = map(lambda x: str(x), G.predecessors(int(node)))
            assert(sorted(parents) == sorted(g.parents(node)))
            children = map(lambda x: str(x), G.successors(int(node)))
            assert(sorted(children) == sorted(g.children(node)))
            ancestors = map(lambda x: str(x), nx.ancestors(G, int(node)))
            assert(sorted(ancestors) == sorted(g.ancestors(node)))
            descendants = map(lambda x: str(x), nx.descendants(G, int(node)))
            assert(sorted(descendants) == sorted(g.descendants(node)))
