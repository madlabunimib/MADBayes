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

    def __eq__(self, other) -> bool:     
        return self._label == other.get_label()

    def __ne__(self, other) -> bool:
        return self._label != other.get_label()


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

    def add_node(self, node: Node) -> None:
        if node not in self._nodes:
            n = len(self._nodes)
            self._adjacency_matrix = np.hstack(
                (
                    self._adjacency_matrix,
                    np.zeros((n,1), dtype=bool)
                ))
            self._adjacency_matrix = np.vstack(
                (
                    self._adjacency_matrix,
                    np.zeros((1,n+1), dtype=bool)
                ))
            self._nodes.append(node)
        else:
            raise Exception("Node already in graph")

    def remove_node(self, node: Node) -> None:
        if node in self._nodes:
            index = self._nodes.index(node)
            self._adjacency_matrix = np.delete(self._adjacency_matrix, index, axis=0)
            self._adjacency_matrix = np.delete(self._adjacency_matrix, index, axis=1)
            self._nodes.remove(node)
        else:
            raise Exception("Node not in graph")

    def add_edge(self, parent: Node, child: Node) -> None:
        if (parent in self._nodes) and (child in self._nodes):
            self._adjacency_matrix[self._nodes.index(parent), self._nodes.index(child)] = True
        else:
            raise Exception("Node not in graph")

    def remove_edge(self, parent: Node, child: Node) -> None:
        if (parent in self._nodes) and (child in self._nodes):
            self._adjacency_matrix[self._nodes.index(parent), self._nodes.index(child)] = False
        else:
            raise Exception("Node not in graph")
