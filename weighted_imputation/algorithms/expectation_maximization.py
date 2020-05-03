from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
import pandas as pd

from .junction_tree import junction_tree
from .nodes import parents as _parents
from ..structures import BayesianNetwork, ConditionalProbabilityTable

if TYPE_CHECKING:
    from typing import Dict, List
    from ..structures import Dataset


def expectation_maximization(dag: BayesianNetwork, dataset: Dataset) -> BayesianNetwork:
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
    dataset = dataset.to_dict('records')
    # Repeat until convergence
    while True:
        ### Expectation Step ###

        # Compute the Junction Tree for exact inference
        jt = junction_tree(dag)
        # Dictionary for computing absolute frequencies
        frequencies = {}
        # For each node, for each row compute absolute
        # frequencies counting from dataset and using
        # joint queries when NAN values are present
        for node in nodes:
            counter = zeros[node].copy()
            for row in dataset:
                # Init query
                query = 1
                # Select variables
                variables = [node] + parents[node]
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
            # Add counter to frequencies
            frequencies[node] = counter

        ### Maximization Step ###

        # For each node update CPT
        frequencies = {
            node: freq / freq.sum(axis=0)
            for node, freq in frequencies.items()
        }
        dag.set_cpts(frequencies)
    return dag


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
        or k != 'count'
        or v is not None
        or not pd.isnull(v)
    }
