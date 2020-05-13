from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..structures import BayesianNetwork, Dataset

from math import lgamma
from itertools import product

from .nodes import parents as _parents


def bds_score(dataset: Dataset, bn: BayesianNetwork, iss: float = 1, with_nodes: bool = False):

    nodes = bn.nodes()
    levels = {node: bn.levels(node) for node in nodes}
    
    score = {
        node : _node_bds_score(node, dataset, bn, iss, levels[node])
        for node in nodes
    }

    if with_nodes:
        return sum(score.values()), score

    return sum(score.values())


def _node_bds_score(node: str, dataset: Dataset, bn: BayesianNetwork, iss: float, levels: list) -> float:
    size = dataset.data.shape[0]

    parents = _parents(bn, node)
    dataset = dataset.absolute_frequencies([node] + parents)
    configs = [((), size)]
    r_i = len(levels)

    q_i = 1
    if len(parents) != 0:
        configs = dataset.groupby(parents).sum()
        configs = [
            (config, value['count'])
            for config, value in configs.iterrows()
        ]
        q_i = len(configs)
        
    score = 0
    for config, n_ij in configs:
        a_ij = iss / q_i
        a_ijk = a_ij / r_i

        score += (lgamma(a_ij) - lgamma(a_ij + n_ij))
        for level in levels:
            n_ijk = _get_n_ijk(dataset, level, config)
            score += (lgamma(a_ijk + n_ijk) - lgamma(a_ijk))

    return score


def _get_n_ijk(dataset, level, config):
    try:
        if not isinstance(level, tuple):
            level = tuple([level])
        if not isinstance(config, tuple):
            config = tuple([config])
        return dataset.loc[level + config]['count']
    except KeyError:
        pass
    return 0
