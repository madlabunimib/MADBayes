from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from ..backends import AlternativeBackend
from .bron_kerbosh import _bron_kerbosh
from .nodes import _perfect_numbering

if TYPE_CHECKING:
    from typing import List
    from ..structures import Graph


@AlternativeBackend()
def chain_of_cliques(graph: Graph) -> List:
    nodes = graph.nodes()
    adjacency_matrix = graph.adjacency_matrix()
    chain = _chain_of_cliques(adjacency_matrix)
    chain = [[nodes[node] for node in clique] for clique in chain]
    return chain

# TODO: Refactor this function
def _chain_of_cliques(A: np.ndarray) -> List:
    raise NotImplementedError('This function MUST be refactored.')
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
    chain = []
    for i in range(n):
        chain.append(cliques[order[i]])
    return chain
