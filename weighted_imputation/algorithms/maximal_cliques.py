from typing import List

from ..structures import Graph
from .bron_kerbosh import bron_kerbosh


def maximal_cliques(graph: Graph) -> List:
    return bron_kerbosh(graph)
