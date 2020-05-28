from __future__ import annotations
from .bds import bds_score, _node_bds_score
from .breadth_first_search import is_reachable
from ..structures import DirectedGraph

from typing import TYPE_CHECKING

from copy import deepcopy
from itertools import product

if TYPE_CHECKING:
    from ..structures import Dataset, BayesianNetwork
    from typing import List


def hill_climbing(dataset: Dataset, score=bds_score, iss: float = 1) -> DirectedGraph:
    nodes = dataset.columns()
    dag_best = DirectedGraph(nodes=nodes)
    score_dag_best = score(dag_best, dataset, iss=iss, with_nodes=True)

    progress = True
    while progress:
        progress = False
        dag = deepcopy(dag_best)
        score_dag = deepcopy(score_dag_best)
        operators = _hc_operators(dag)
        for operator, edge in operators:
            dag_o = deepcopy(dag)
            o = getattr(dag_o, operator)
            if _hc_legal_solution(dag_o, operator, edge):
                o(*edge)
                score_dag_o = _hc_score(
                    dag_o, dataset, operator, edge, score_dag, iss)
                if score_dag_o[0] > score_dag_best[0]:
                    progress = True
                    dag_best = dag_o
                    score_dag_best = score_dag_o
    return dag_best


def _hc_score(network: BayesianNetwork, dataset: Dataset, operator: str, edge: Tuple, score, iss: float):

    nodes_scores = deepcopy(score[1])
    # If we add or remove an edge we need only to update the child's score value
    if operator == "add_edge" or operator == "remove_edge":
        levels = dataset.levels()[edge[1]]
        nodes_scores[edge[1]] = _node_bds_score(
            edge[1], dataset, network, iss, levels)
        return (sum(nodes_scores.values()), nodes_scores)

    # If we revert an edge we need to update both nodes
    else:
        levels = dataset.levels()[edge[1]]
        nodes_scores[edge[1]] = _node_bds_score(
            edge[1], dataset, network, iss, levels)
        levels = dataset.levels()[edge[0]]
        nodes_scores[edge[0]] = _node_bds_score(
            edge[0], dataset, network, iss, levels)
        return (sum(nodes_scores.values()), nodes_scores)


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
    return operator == 'remove_edge' or not is_reachable(dag, edge)
