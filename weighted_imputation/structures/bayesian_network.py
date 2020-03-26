from typing import Dict, List

import numpy as np
import pandas as pd
import xarray as xa

from ..io import parse_network_file
from .conditional_probability_table import CPT
from .graph import DirectedGraph


class BayesianNetwork(DirectedGraph):

    def __init__(self, nodes: List[str] = None, adjacency_matrix: np.ndarray = None) -> None:
        super().__init__(nodes, adjacency_matrix)
    
    @classmethod
    def from_file(cls, path: str) -> None:
        parsed = parse_network_file(path)
        n = len(parsed.keys())
        nodes = list(parsed.keys())
        adjacency_matrix = np.zeros((n, n), dtype=bool)
        for key, value in parsed.items():
            child = nodes.index(key)
            for dependency in value['dependencies']:
                parent = nodes.index(dependency)
                adjacency_matrix[parent, child] = True
        bn = cls(nodes, adjacency_matrix)
        for key, value in parsed.items():
            variables = [key]
            levels = [value['levels']]
            if len(value['dependencies']) == 0:
                data = [([value['levels'][i]], v) for i, v in enumerate(value['cpt'][0])]
            else:
                variables += value['dependencies']
                levels += [parsed[dependency]['levels'] for dependency in value['dependencies']]
                data = [
                    ([value['levels'][i]] + row[0], v)
                    for row in value['cpt']
                    for i, v in enumerate(row[1])
                ]
            array = xa.DataArray(dims=variables, coords=levels)
            for (location, value) in data:
                array.loc[location] = value
            bn[key]['CPT'] = CPT(array)
        return bn
    
    @classmethod
    def _load_dataset(cls, graph: DirectedGraph, dataset: str):
        df = pd.read_csv(dataset)
        if set(graph.get_nodes()) != set(df.columns):
            raise Exception('structure and dataset variables are different.')
        for node in graph.get_nodes():
            graph[node]['RFT'] = df[node].value_counts() / df[node].size
        return graph
    
    @classmethod
    def from_structure_and_dataset(cls, structure: str, dataset: str):
        graph = cls.from_structure(structure)
        graph = cls._load_dataset(graph, dataset)
        return graph
