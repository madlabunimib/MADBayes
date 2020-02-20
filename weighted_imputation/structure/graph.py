from typing import List, Dict
import numpy as np
import pandas as pd


class Graph():

    _adjacency_matrix: pd.DataFrame

    def __init__(self, adjacency_matrix: np.ndarray) -> None:
        self.set_adjacency_matrix(adjacency_matrix)

    def __init__(self, nodes: List[str], adjacency_matrix: np.ndarray) -> None:
        self.set_adjacency_matrix(adjacency_matrix)
        self.set_nodes(nodes)

    def get_nodes(self) -> List[str]:
        return list(self._adjacency_matrix.index.values)
    
    def set_nodes(self, nodes: List[str]) -> "Graph":
        if self._adjacency_matrix.shape[0] != len(nodes):
            raise Exception('nodes must have the same length of adjacent_matrix.')
        # In order to set the labels, a mapping between old labels and
        # new labels must be created
        labels = self.get_nodes()
        mapping = {
            label: nodes[i]
            for i, label in enumerate(labels)
        }
        self._adjacency_matrix.rename(index=mapping, columns=mapping, inplace=True)
        return self

    def get_adjacency_matrix(self) -> np.ndarray:
        return self._adjacency_matrix.to_numpy(dtype=bool, copy=True)
    
    def set_adjacency_matrix(self, adjacency_matrix: np.ndarray) -> "Graph":
        if len(adjacency_matrix.shape) != 2:
            raise Exception('adjacency_matrix must be a 2D matrix.')
        if adjacency_matrix.shape[0] == 0:
            raise Exception('adjacency_matrix must be a valid matrix.')
        if adjacency_matrix.shape[0] != adjacency_matrix.shape[1]:
            raise Exception('adjacency_matrix must be a square matrix.')
        if adjacency_matrix.dtype != bool:
            raise Exception('adjacency_matrix must be a boolean matrix.')        
        if self._adjacency_matrix is not None:
            if self._adjacency_matrix.shape != adjacency_matrix.shape:
                raise Exception('adjacency_matrix must have the same shape of current matrix.')
            else:
                # If the adjacency_matrix is already defined and has the same
                # shape of the new adjacency_matrix, create a new matrix using
                # the new data and keeping the previous node names
                nodes = self.get_nodes()
                self._adjacency_matrix.shape = pd.DataFrame(
                    data=adjacency_matrix,
                    index=nodes,
                    columns=nodes,
                    dtype=bool,
                    copy=True
                )
        else:
            # If there is no adjacency_matrix, create a new one without specify
            # the labels of the nodes
            self._adjacency_matrix.shape = pd.DataFrame(
                data=adjacency_matrix,
                dtype=bool,
                copy=True
            )
        return self

    def add_node(self, node: str) -> "Graph":
        self._adjacency_matrix.loc[node, :] = False
        self._adjacency_matrix.loc[:, node] = False
        self._adjacency_matrix.sort_index(axis=0, inplace=True)
        self._adjacency_matrix.sort_index(axis=1, inplace=True)
        return self

    def remove_node(self, node: str) -> "Graph":
        self._adjacency_matrix.drop(node, axis=0, inplace=True)
        self._adjacency_matrix.drop(node, axis=1, inplace=True)
        return self

    def add_edge(self, parent: str, child: str) -> "Graph":
        self._adjacency_matrix.loc[parent, child] = True
        return self

    def remove_edge(self, parent: str, child: str) -> "Graph":
        self._adjacency_matrix.loc[parent, child] = False
        return self
