from __future__ import annotations

from typing import TYPE_CHECKING

from .bron_kerbosh import bron_kerbosh

if TYPE_CHECKING:
    from typing import List
    from ..structures import Graph


def maximal_cliques(graph: Graph) -> List:
    return bron_kerbosh(graph)
