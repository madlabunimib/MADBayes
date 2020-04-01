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

def _chain_of_cliques(A: np.ndarray) -> List:
    # Calculate the perfect numbering
    # starting from the first node
    numbering = _perfect_numbering(0, A)
    # Calculate the list of maximal cliques
    # using the Bron-Kerbosh algorithm
    cliques = _bron_kerbosh(A)
    # Assign to each clique the largest perfect
    # number of its nodes
    chain = {
        i: max([
            np.nonzero(numbering == node)[0]
            for node in clique
        ])
        for i, clique in enumerate(cliques)
    }
    chain = sorted(chain, key=chain.get)
    chain = [cliques[i] for i in chain]
    return chain
