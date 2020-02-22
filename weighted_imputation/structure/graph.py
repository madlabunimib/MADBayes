import re
import numpy as np
import pandas as pd
import networkx as nx
from typing import List, Dict


class Graph():

    _adjacency_matrix: pd.DataFrame

    def __init__(self, nodes: List[str] = None, adjacency_matrix: np.ndarray = None) -> None:
        if nodes is not None:
            self.set_nodes(nodes)
        if adjacency_matrix is not None:
            self.set_adjacency_matrix(adjacency_matrix)
        if nodes is None and adjacency_matrix is None:
            self._adjacency_matrix = pd.DataFrame(dtype=bool)

    def get_nodes(self) -> List[str]:
        return list(self._adjacency_matrix.index.values)
    
    def set_nodes(self, nodes: List[str]) -> "Graph":
        try:
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
        except AttributeError:
            # If there is no adjacency_matrix, create a new empty one using
            # the labels of the nodes
            n = len(nodes)
            self._adjacency_matrix = pd.DataFrame(
                data=np.zeros((n, n), dtype=bool),
                index=nodes,
                columns=nodes
            )
        return self

    def get_adjacency_matrix(self) -> np.ndarray:
        return self._adjacency_matrix.to_numpy(dtype=bool, copy=True)
    
    def set_adjacency_matrix(self, adjacency_matrix: np.ndarray) -> "Graph":
        if len(adjacency_matrix.shape) != 2:
            raise Exception('adjacency_matrix must be a 2D matrix.')
        if adjacency_matrix.shape[0] != adjacency_matrix.shape[1]:
            raise Exception('adjacency_matrix must be a square matrix.')
        if adjacency_matrix.dtype != bool:
            raise Exception('adjacency_matrix must be a boolean matrix.')        
        try:
            if self._adjacency_matrix.shape != adjacency_matrix.shape:
                raise Exception('adjacency_matrix must have the same shape of current matrix.')
            else:
                # If the adjacency_matrix is already defined and has the same
                # shape of the new adjacency_matrix, create a new matrix using
                # the new data and keeping the previous node names
                nodes = self.get_nodes()
                self._adjacency_matrix = pd.DataFrame(
                    data=adjacency_matrix,
                    index=nodes,
                    columns=nodes,
                    dtype=bool,
                    copy=True
                )
        except AttributeError:
            # If there is no adjacency_matrix, create a new one without specify
            # the labels of the nodes
            self._adjacency_matrix = pd.DataFrame(
                data=adjacency_matrix,
                dtype=bool,
                copy=True
            )
        return self

    def add_node(self, node: str) -> "Graph":
        self._adjacency_matrix.loc[node, :] = False
        self._adjacency_matrix.loc[:, node] = False
        return self

    def remove_node(self, node: str) -> "Graph":
        self._adjacency_matrix.drop(node, axis=0, inplace=True)
        self._adjacency_matrix.drop(node, axis=1, inplace=True)
        return self

    def add_edge(self, parent: str, child: str, undirected: bool = False) -> "Graph":
        if parent not in self._adjacency_matrix or child not in self._adjacency_matrix:
            raise Exception('parent and child nodes must be in adjacency_matrix before adding edge.')
        self._adjacency_matrix.loc[parent, child] = True
        if undirected:
            self._adjacency_matrix.loc[child, parent] = True
        return self

    def remove_edge(self, parent: str, child: str, undirected: bool = False) -> "Graph":
        if parent not in self._adjacency_matrix or child not in self._adjacency_matrix:
            raise Exception('parent and child nodes must be in adjacency_matrix before removing edge.')
        self._adjacency_matrix.loc[parent, child] = False
        if undirected:
            self._adjacency_matrix.loc[child, parent] = False
        return self

    def __repr__(self):
        return str(self._adjacency_matrix)
    
    def is_undirected(self) -> bool:
        adjacency_matrix = self.get_adjacency_matrix()
        return np.allclose(adjacency_matrix, adjacency_matrix.T)
    
    def to_networkx(self) -> nx.Graph:
        mapping = {k:v for k,v in enumerate(self.get_nodes())}
        G = nx.DiGraph(self.get_adjacency_matrix())
        G = nx.relabel_nodes(G, mapping)
        return G

    def to_networkx_undirected(self) -> nx.Graph:
        mapping = {k:v for k,v in enumerate(self.get_nodes())}
        G = nx.Graph(self.get_adjacency_matrix())
        G = nx.relabel_nodes(G, mapping)
        return G
    
    @classmethod
    def from_networkx(cls, G: nx.Graph) -> "Graph":
        nodes = [str(node) for node in G.nodes]
        adjacent_matrix = nx.to_numpy_array(G).astype(bool)
        return cls(nodes, adjacent_matrix)
    
    @classmethod
    def from_string(cls, string: str) -> "Graph":
        pattern = re.compile(r"\[(\w*)(?:\|(\w+[:\w+]*)){0,1}\]")
        edges = re.findall(pattern, string)
        edges = [
            (parent, child)
            for (child, parents) in edges
            for parent in parents.split(':')
            if len(parent) > 0
        ]
        nodes = set()
        for parent, child in edges:
            nodes.add(parent)
            nodes.add(child)
        nodes = sorted(nodes)
        graph = cls(nodes)
        for parent, child in edges:
            graph.add_edge(parent, child)
        return graph
