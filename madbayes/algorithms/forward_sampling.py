from __future__ import annotations

from typing import TYPE_CHECKING

import pandas as pd
from random import uniform
from multiprocessing import Pool, cpu_count
from copy import deepcopy

from ..structures import DirectedGraph, BayesianNetwork, Dataset
from .nodes import parents, children

if TYPE_CHECKING:
    from typing import List, Set
    from ..structures import Node


def forward_sampling(bn: BayesianNetwork, n_samples: int):
    order = _find_order(bn)

    params = [
        (bn, order)
        for _ in range(n_samples)
    ]
    pool = Pool(cpu_count())
    samples = pool.starmap(_sample, params)
    pool.close()
    pool.join()

    return Dataset(pd.concat(samples, axis=1).T)


def _sample(bn: BayesianNetwork, order: List):
    sample = pd.Series(index=order, dtype=str)
    for var in order:
        filter = {dim: sample[dim]
                  for dim in bn[var]["CPT"].variables() if dim != var}
        probs = bn[var]["CPT"].sel(filter)

        num = uniform(0, 1)
        cum_prob = 0
        for i in range(len(probs)):
            cum_prob += probs[i]
            if num <= cum_prob:
                sample._set_value(var, bn[var]["CPT"].levels(var)[i])
                break
    return sample


def _find_order(dag: DirectedGraph) -> List:
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
