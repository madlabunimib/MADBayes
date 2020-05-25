from __future__ import annotations

from typing import TYPE_CHECKING
from .nodes import children

if TYPE_CHECKING:
    from typing import Dict
    from ..structures import Graph, Node


def BFS(graph: Graph) -> Dict:
    pass

# Use BFS to check path between parent and child


def is_reachable(graph: Graph, edge):

    visited = {node: False for node in graph.nodes()}

    queue = []
    queue.append(edge[1])
    visited[edge[1]] = True

    while queue:
        node = queue.pop(0)

        if node == edge[0]:
            return True

        for child in children(graph, node):
            if visited[child] == False:
                queue.append(child)
                visited[child] = True

    return False
