from __future__ import annotations

from typing import TYPE_CHECKING

from .maximum_cardinality_search import MCS

if TYPE_CHECKING:
    from ..structures import Graph

def triangulate(graph: Graph):
    return MCS(graph)
