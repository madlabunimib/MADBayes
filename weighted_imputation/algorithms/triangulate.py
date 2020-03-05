from .maximum_cardinality_search import MCS
from ..structures import Graph

def triangulate(graph: Graph):
    return MCS(graph)
