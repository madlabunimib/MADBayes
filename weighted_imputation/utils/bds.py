import numpy as np
from math import lgamma
from itertools import product

from ..data import load_datasets_from_disk
from ..structures import BayesianNetwork, Dataset
from ..algorithms import parents as _parents


def bds_score(dataset: str, bn: BayesianNetwork, iss: float, DEBUG: bool):

    dataset = load_datasets_from_disk()[dataset]
    nodes = bn.nodes()
    nodes_levels = {node: bn.levels(node) for node in nodes}
    
    score = {node : node_bds_score(dataset, bn, iss, nodes_levels[node], node) for node in nodes}
    if DEBUG:
        from pprint import pprint
        pprint(score)
    
    return sum(score.values())


def node_bds_score(dataset: Dataset, bn: BayesianNetwork, iss: float, levels: dict, node) -> float:
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

        score += (lgamma(a_ij) - lgamma(a_ij + n_ij))               # outer product/sum
        for level in levels:
            n_ijk = _get_n_ijk(dataset, level, config)
            score += (lgamma(a_ijk + n_ijk) - lgamma(a_ijk))        # inner product/sum

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
