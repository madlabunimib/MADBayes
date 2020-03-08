import numpy as np
import pandas as pd
from typing import Dict, List
from .graph import DirectedGraph
from ..io import  parse_network_file, build_cpt


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
            bn[key]['cpt'] = build_cpt(key, value)
        return bn
