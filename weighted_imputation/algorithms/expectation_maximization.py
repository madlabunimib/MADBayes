from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
import pandas as pd
from os import sched_getaffinity
from multiprocessing import Pool

from .junction_tree import junction_tree
from .nodes import parents as _parents
from ..structures import BayesianNetwork, ConditionalProbabilityTable

if TYPE_CHECKING:
    from typing import Dict, List
    from ..structures import Dataset


def expectation_maximization(
    dag: BayesianNetwork,
    dataset: Dataset,
    max_iter: int = 50,
    rtol: float = 1e-05,
    atol: float = 1e-08
) -> BayesianNetwork:
    # If DAG is string, buld BayesianNetwork
    if isinstance(dag, str):
        dag = BayesianNetwork.from_structure(dag)
    # Get nodes from dag
    nodes = dag.nodes()
    # Get variables levels from dataset
    levels = dataset.levels()
    # Cache parents for each node
    parents = {
        node: _parents(dag, node)
        for node in nodes
    }
    # Create zeroed CPTs for each variable
    zeros = _build_empty_cpts(nodes, levels, parents)
    # Initialize CPTs of each node
    # using a uniform distribution
    for node in nodes:
        dag[node]['CPT'] = zeros[node] + (1 / len(levels[node]))
    # Count absolute frequencies of unique
    # variables configurations in dataset
    # and transform in list of dicts by row
    dataset = dataset.absolute_frequencies()
    dataset = dataset.reset_index().to_dict('records')
    # Repeat until convergence or max iterations reached
    iteration = 0
    converged = False
    while not converged and iteration < max_iter:
        ### Expectation Step ###

        # Compute the Junction Tree for exact inference
        jt = junction_tree(dag)
        # Initialize list of parameters
        frequencies = [
            (node, parents[node], dataset, zeros[node].copy(), jt)
            for node in nodes
        ]
        # For each node, for each row compute absolute
        # frequencies counting from dataset and using
        # joint queries when NAN values are present
        pool = Pool(len(sched_getaffinity(0)))
        frequencies = pool.starmap(_expectation_maximization_node, frequencies)
        pool.close()
        pool.join()

        ### Maximization Step ###

        # For each node compute CPT
        frequencies = {
            nodes[i]: freq / freq.sum(axis=0)
            for i, freq in enumerate(frequencies)
        }

        ### Check stopping criteria ###
        converged = _has_converged(dag, frequencies, rtol, atol)
        iteration += 1

        # Update CPT in DAG
        dag.set_cpts(frequencies)
    return dag


def _expectation_maximization_node(node, parents, dataset, counter, jt):
    for row in dataset:
        # Init query
        query = 1
        # Select variables
        variables = [node] + parents
        # Select variables values
        values = {
            k: v for k, v in row.items()
            if k in variables
        }
        # Check if there are NAN values
        any_nan = any([pd.isnull(v) for _, v in values.items()])
        if (any_nan):
            # Set evidence
            evidence = _build_evidence(row, variables)
            jte = jt.set_evidence(**evidence)
            # Execute query
            query = jte.query('joint', variables)[0]
        # Update values
        counter.loc[values] += query * row['count']
    return counter


def _build_empty_cpts(nodes: List, levels: Dict, parents: Dict):
    cpts = {}
    for node in nodes:
        dim = [node] + parents[node]
        lvs = [levels[d] for d in dim]
        dat = np.zeros([len(l) for l in lvs])
        cpts[node] = ConditionalProbabilityTable(
            data=dat,
            dims=dim,
            coords=lvs
        )
    return cpts


def _build_evidence(row: Dict, variables: List):
    return {
        k: v for k, v in row.items()
        if k not in variables
        and k != 'count'
        and not pd.isnull(v)
    }


def _has_converged(dag: BayesianNetwork, frequencies: Dict, rtol: float, atol: float):
    return all([
        np.allclose(
            dag[node]['CPT'].values,
            cpt.values,
            rtol=rtol,
            atol=atol
        )
        for node, cpt in frequencies.items()
    ])
