import networkx as nx
from functools import reduce
from . import madbayes as mb


def test_structure_chain_of_cliques():
    for nodes in [10, 25, 50, 100]:
        g = mb.Graph.random(nodes, 0.5)
        g = mb.chordal(g)
        cliques = mb.maximal_cliques(g)
        alpha = mb.maximum_cardinality_search(g)
        chain = mb.chain_of_cliques(cliques, alpha)
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
