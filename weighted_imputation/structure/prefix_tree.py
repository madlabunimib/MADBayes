import numpy as np
from typing import List

class Prefix_tree():

    _nodes: List[int]
    _adjacency_matrix: np.ndarray

    def __init__(self, nodes: List[int], adjacency_matrix: np.ndarray) -> None:
        self.set_nodes(nodes)
        self.set_adjacency_matrix(adjacency_matrix)

    def get_nodes(self) -> List[int]:
        return self._nodes
    
    def set_nodes(self, nodes: List[int]) -> None:
        self._nodes = nodes

    def get_adjacency_matrix(self) -> np.ndarray:
        return self._adjacency_matrix
    
    def set_adjacency_matrix(self, adjacency_matrix: np.ndarray) -> None:
        self._adjacency_matrix = adjacency_matrix

    def add_node(self, node: int) -> None:
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

    def remove_node(self, node: int) -> None:
        if node in self._nodes:
            index = self._nodes.index(node)
            self._adjacency_matrix = np.delete(self._adjacency_matrix, index, axis=0)
            self._adjacency_matrix = np.delete(self._adjacency_matrix, index, axis=1)
            self._nodes.remove(node)
        else:
            raise Exception("int not in graph")

    def add_edge(self, parent: int, child: int) -> None:
        if (parent in self._nodes) and (child in self._nodes):
            self._adjacency_matrix[self._nodes.index(parent), self._nodes.index(child)] = True
        else:
            raise Exception("int not in graph")

    def remove_edge(self, parent: int, child: int) -> None:
        if (parent in self._nodes) and (child in self._nodes):
            self._adjacency_matrix[self._nodes.index(parent), self._nodes.index(child)] = False
        else:
            raise Exception("int not in graph")