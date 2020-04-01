import networkx as nx
from functools import reduce
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
    chains = [wi.chain_of_cliques(graph) for graph in graphs]
    chains = [[set(clique) for clique in chain] for chain in chains]
    running = [
        [
            chain[i].intersection(
                reduce(lambda a,b: a.union(b), chain[:i], set())
            )
            for i, _ in enumerate(chain)
        ]
        for chain in chains
    ]
    running = [
        all([
            any([
                run.issubset(set(clique))
                for clique in chains[i]
            ])
            for run in runs
        ])
        for i, runs in enumerate(running)
    ]
    assert(all(running))
