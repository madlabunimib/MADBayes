import numpy as np
from typing import List, Set
from ..structure import Graph


def maximal_cliques(graph: Graph) -> List:
    nodes = graph.get_nodes()
    nodes_indexes = [i for i, _ in enumerate(nodes)]
    adjacency_matrix = graph.get_adjacency_matrix()
    maximal_cliques = _bron_kerbosh(adjacency_matrix, set(), set(nodes_indexes), set())
    maximal_cliques = [
        [nodes[node] for node in maximal_clique]
        for maximal_clique in maximal_cliques
    ]
    return maximal_cliques

def _neighbor_set(adjacency_matrix: np.ndarray, node: int) -> Set[int]:
    return set(np.argwhere(adjacency_matrix[node]).T[0])

# Reference function: networkx.algorithms.clique.find_cliques
def _bron_kerbosh(adjacency_matrix: np.ndarray, A: Set[int], B: Set[int], C: Set[int]) -> List:
    #   if B and C are empty:
    #       return A
    #   foreach node in B do:
    #       _bron_kerbosh(
    #           union(A, {node}),
    #           intersect(B, _neighbor_set(adjacency_matrix, node)),
    #           intersect(C, _neighbor_set(adjacency_matrix, node))
    #       )
    #       B := difference(B, {node})
    #       C := union(C, {node})
    pass
