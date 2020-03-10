import numpy as np
from numba import njit
from numba.typed import List
from typing import List
from .bron_kerbosh import _bron_kerbosh
from .nodes import _perfect_numbering
from ..structures import Graph


def chain_of_cliques(graph: Graph) -> List:
    nodes = graph.get_nodes()
    adjacency_matrix = graph.get_adjacency_matrix()
    chain = _chain_of_cliques(adjacency_matrix)
    chain = [[nodes[node] for node in clique] for clique in chain]
    return chain

# @njit
def _chain_of_cliques(A: np.ndarray) -> List:
    # Calculate the perfect numbering
    # starting from the first node
    numbering = _perfect_numbering(0, A)
    # Calculate the list of maximal cliques
    # using the Bron-Kerbosh algorithm
    cliques = _bron_kerbosh(A)
    # Assign to each clique the largest perfect
    # number of its nodes
    n = len(cliques)
    order = np.zeros(n)
    for i in range(n):
        clique = cliques[i]
        vmax = 0
        for node in clique:
            number = np.nonzero(numbering == node)[0]
            if vmax < number:
                vmax = number
        order[i] = vmax
    order = np.argsort(order)
    chain = list()
    for i in range(n):
        chain.append(cliques[order[i]])
    return chain
