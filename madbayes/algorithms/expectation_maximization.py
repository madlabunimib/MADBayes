from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
import pandas as pd
from copy import deepcopy
from scipy.special import rel_entr as kl
from multiprocessing import Pool, cpu_count

from .junction_tree import junction_tree
from .nodes import parents as _parents
from ..structures import DirectedGraph, BayesianNetwork, ConditionalProbabilityTable

if TYPE_CHECKING:
    from typing import Dict, List
    from ..structures import Dataset


def expectation_maximization(
    dag: DirectedGraph,
    dataset: Dataset,
    max_iter: int = 50,
    tol: float = 1e-08
) -> BayesianNetwork:
    # If DAG is string, build BayesianNetwork
    if isinstance(dag, str):
        dag = BayesianNetwork.from_structure(dag)
    if isinstance(dag, DirectedGraph):
        dag = BayesianNetwork(
            nodes=dag.nodes(),
            adjacency_matrix=dag.adjacency_matrix()
        )
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
        pool = Pool(cpu_count())
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
        converged = _has_converged(dag, frequencies, tol)
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


def _has_converged(dag: BayesianNetwork, frequencies: Dict, tol: float):
    return all([
        np.sum(kl(dag[node]['CPT'].values, cpt.values)) < tol
        for node, cpt in frequencies.items()
    ])
