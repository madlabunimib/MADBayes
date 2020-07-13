import networkx as nx
from functools import reduce
from . import madbayes as mb


def test_chain_of_cliques():
    for nodes in [10, 25, 50, 100]:
        g = mb.backend.Graph.random(nodes, 0.5)
        g = mb.backend.chordal(g)
        cliques = mb.backend.maximal_cliques(g)
        alpha = mb.backend.maximum_cardinality_search(g)
        chain = mb.backend.chain_of_cliques(cliques, alpha)
        chain = [set(clique) for clique in chain]
        running = [
            chain[i].intersection(
                reduce(lambda a, b: a.union(b), chain[:i], set())
            )
            for i, _ in enumerate(chain)
        ]
        running = any([
            run.issubset(set(run))
            for run in running
        ])
        assert(running)
