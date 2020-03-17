from ..structures import Graph
from .maximum_cardinality_search import MCS


def triangulate(graph: Graph):
    return MCS(graph)
