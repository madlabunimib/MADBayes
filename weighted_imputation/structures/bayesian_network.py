import numpy as np
import pandas as pd
from typing import Dict, List
from .graph import DirectedGraph
from .conditional_probability_table import CPT
from ..io import  parse_network_file


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
            if len(value['dependencies']) == 0:
                data = np.array(value['cpt'][0])
                tuples = None
            else:
                data = np.array([row[1] for row in value['cpt']])
                tuples = [tuple(row[0]) for row in value['cpt']]
            bn[key]['CPT'] = CPT(key, value['dependencies'], data, value['levels'], tuples)
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
    def from_file_and_dataset(cls, file: str, dataset: str):
        graph = cls.from_file(file)
        graph = cls._load_dataset(graph, dataset)
        return graph
    
    @classmethod
    def from_structure_and_dataset(cls, structure: str, dataset: str):
        graph = cls.from_structure(structure)
        graph = cls._load_dataset(graph, dataset)
        return graph
