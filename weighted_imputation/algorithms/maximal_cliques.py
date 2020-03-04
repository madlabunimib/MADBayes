from typing import List
from .bron_kerbosh import bron_kerbosh
from ..structures import Graph


def maximal_cliques(graph: Graph) -> List:
    return bron_kerbosh(graph)
