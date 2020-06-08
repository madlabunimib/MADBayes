from __future__ import annotations

import numpy as np

from scipy.special import rel_entr as kl

from .expectation_maximization import expectation_maximization
from .hill_climbing import hill_climbing
from .impute import impute
from .junction_tree import junction_tree
from ..structures import DirectedGraph

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..structures import Dataset


def structural_em(
    dataset: Dataset,
    max_iter: int = 50,
    tol: float = 1e-08
) -> BayesianNetwork:
    imputed = dataset
    dag = DirectedGraph(dataset.columns())
    bn = expectation_maximization(dag, imputed)

    iteration = 0
    converged = False
    while not converged and iteration < max_iter:
        ### Expectation Step ###
        imputed = impute(bn, dataset)

        ### Maximization Step ###
        dag = hill_climbing(imputed)
        bn_next = expectation_maximization(dag, imputed)

        converged = _has_converged(bn, bn_next, tol)
        iteration += 1

        bn = bn_next

    return bn


def _has_converged(bn: BayesianNetwork, bn_next: BayesianNetwork, tol: float):
    return all([
        np.sum(kl(bn[node]['CPT'].values, bn_next[node]['CPT'].values)) < tol
        for node in bn_next.nodes()
    ])
