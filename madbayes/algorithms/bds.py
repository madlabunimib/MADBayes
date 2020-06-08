from __future__ import annotations
from .nodes import parents as _parents
from ..structures import BayesianNetwork
from multiprocessing import Pool, cpu_count
from math import lgamma

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..structures import Dataset


def bds_score(network: BayesianNetwork, dataset: Dataset, iss: float = 1, with_nodes: bool = False):
    # If network is string, buld BayesianNetwork
    if isinstance(network, str):
        network = BayesianNetwork.from_structure(network)

    nodes = sorted(network.nodes())

    score = [
        (node, dataset, network, iss)
        for node in nodes
    ]

    pool = Pool(cpu_count())
    score = pool.starmap(_node_bds_score, score)
    pool.close()
    pool.join()

    score = {
        node: score[i]
        for i, node in enumerate(nodes)
    }

    if with_nodes:
        return sum(score.values()), score

    return sum(score.values())


def _node_bds_score(node: str, dataset: Dataset, network: BayesianNetwork, iss: float) -> float:
    size = dataset.data.shape[0]
    levels = dataset.levels(node)

    parents = _parents(network, node)
    dataset = dataset.absolute_frequencies([node] + parents)
    configs = [((), size)]
    r_i = len(levels)

    q_i = 1
    if len(parents) > 0:
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
            n_ijk = _n_ijk(dataset, level, config)
            score += (lgamma(a_ijk + n_ijk) - lgamma(a_ijk))

    return score


def _n_ijk(dataset, level, config):
    try:
        if not isinstance(level, tuple):
            level = tuple([level])
        if not isinstance(config, tuple):
            config = tuple([config])
        return dataset.loc[level + config]['count']
    except KeyError:
        pass
    return 0
