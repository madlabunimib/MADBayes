from typing import List, Dict
import numpy as np


class Node():

    _label: str
    _values: Dict

    def __init__(self, label: str) -> None:
        self.set_label(label)
        self._values = {}

    def get_label(self) -> str:
        return self._label
    
    def set_label(self, label: str) -> None:
        self._label = label

    def get_values(self) -> Dict:
        return self._values
    
    def set_values(self, values: Dict) -> None:
        self._values = values
    
    def __str__(self) -> str:
        return self._label
    
    def __repr__(self) -> str:
        return self._label


class Graph():

    _nodes: List[Node]
    _adjacency_matrix: np.ndarray

    def __init__(self, nodes: List[Node], adjacency_matrix: np.ndarray) -> None:
        self.set_nodes(nodes)
        self.set_adjacency_matrix(adjacency_matrix)

    def get_nodes(self) -> List[Node]:
        return self._nodes
    
    def set_nodes(self, nodes: List[Node]) -> None:
        self._nodes = nodes

    def get_adjacency_matrix(self) -> np.ndarray:
        return self._adjacency_matrix
    
    def set_adjacency_matrix(self, adjacency_matrix: np.ndarray) -> None:
        self._adjacency_matrix = adjacency_matrix
