from __future__ import annotations
from .bds import bds_score
from .breadth_first_search import is_reachable
from ..structures import DirectedGraph

from typing import TYPE_CHECKING

from copy import deepcopy
from itertools import product

if TYPE_CHECKING:
    from ..structures import Dataset
    from typing import List


def hill_climbing(dataset: Dataset, score=bds_score) -> DirectedGraph:
    nodes = dataset.columns()
    dag_best = DirectedGraph(nodes=nodes)
    score_dag_best = score(dag_best, dataset)

    progress = True
    while progress:
        progress = False
        dag = deepcopy(dag_best)
        operators = _hc_operators(dag)
        for operator, edge in operators:
            dag_o = deepcopy(dag)
            o = getattr(dag_o, operator)
            if _hc_legal_solution(dag_o, operator, edge):
                o(*edge)
                score_dag_o = score(dag_o, dataset)
                if score_dag_o > score_dag_best:
                    progress = True
                    dag_best = dag_o
                    score_dag_best = score_dag_o
    return dag_best


def _hc_operators(dag: DirectedGraph) -> List[Tuple]:
    operators = ['add_edge', 'remove_edge', 'reverse_edge']
    edges = [
        [
            edge
            for edge in dag.missing_edges()
            if edge[0] != edge[1]
        ],
        dag.edges(),
        [
            (edge[1], edge[0])
            for edge in dag.edges()
        ]
    ]
    operators = [
        o
        for i, operator in enumerate(operators)
        for o in list(product([operator], edges[i]))
    ]
    return operators


def _hc_legal_solution(dag, operator, edge):
    return operator != 'remove_edge' and not is_reachable(dag, edge)
