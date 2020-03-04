from .maximum_cardinality_search import maximum_cardinality_search_fill_in
from ..structures import Graph

def triangulate(graph: Graph):
    return maximum_cardinality_search_fill_in(graph)
