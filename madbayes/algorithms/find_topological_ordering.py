from __future__ import annotations

from typing import TYPE_CHECKING

from copy import deepcopy

from ..structures import DirectedGraph
from .nodes import parents, children

if TYPE_CHECKING:
    from typing import List, Set
    from ..structures import Node


def find_topological_order(dag: DirectedGraph) -> List:
    tmp_dag = deepcopy(dag)
    order = []
    visited = set()
    # Start with a random node
    _find_order_rec(tmp_dag, dag.nodes()[0], order, visited)
    return order


def _find_order_rec(dag: DirectedGraph, node: Node, order: List, visited: Set) -> None:
    try:
        parents_list = parents(dag, node)
        while len(parents_list) > 0:
            parent = parents_list.pop()
            _find_order_rec(dag, parent, order, visited)

        if node not in visited:
            visited.add(node)
            order.append(node)
            children_list = children(dag, node)
            dag.remove_node(node)

            while len(children_list) > 0:
                child = children_list.pop()
                _find_order_rec(dag, child, order, visited)
    except:
        pass
