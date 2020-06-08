import re
from copy import deepcopy
from typing import Dict, List, Tuple

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd


class Graph():

    _nodes_attributes: Dict
    _adjacency_matrix: pd.DataFrame

    def __init__(self, nodes: List[str] = None, adjacency_matrix: np.ndarray = None) -> None:
        self._nodes_attributes = {}
        if nodes is not None:
            self.set_nodes(nodes)
        if adjacency_matrix is not None:
            self.set_adjacency_matrix(adjacency_matrix)
        if nodes is None and adjacency_matrix is None:
            self._adjacency_matrix = pd.DataFrame(dtype=bool)
    
    def __len__(self) -> int:
        return len(self.nodes())

    def __getitem__(self, key) -> Dict:
        if not key in self.nodes():
            raise KeyError('node not in graph.')
        if not key in self._nodes_attributes.keys():
            self._nodes_attributes[key] = {}
        return self._nodes_attributes[key]

    def __setitem__(self, key, value) -> None:
        if not key in self.nodes():
            raise KeyError('node not in graph.')
        self._nodes_attributes[key] = value

    def __delitem__(self, key) -> None:
        del(self._nodes_attributes[key])

    def __iter__(self):
        return self._nodes_attributes.items().__iter__()

    def nodes(self) -> List[str]:
        return list(self._adjacency_matrix.index.values)
    
    def edges(self) -> List[Tuple[str]]:
        edges = self._adjacency_matrix.stack()
        edges = edges[edges == True].index.tolist()
        return edges
    
    def missing_edges(self) -> List[Tuple[str]]:
        edges = self._adjacency_matrix.stack()
        edges = edges[edges == False].index.tolist()
        return edges
    
    def set_nodes(self, nodes: List[str]) -> "Graph":
        try:
            if self._adjacency_matrix.shape[0] != len(nodes):
                raise Exception('nodes must have the same length of adjacent_matrix.')
            # In order to set the labels, a mapping between old labels and
            # new labels must be created
            mapping = {
                label: nodes[i]
                for i, label in enumerate(self.nodes())
            }
            # Remapping nodes attributes
            self._nodes_attributes = {
                value: self[key]
                for key, value in mapping.items()
            }
            # Remapping adjacency matrix
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

    def adjacency_matrix(self, copy: bool = True) -> np.ndarray:
        return self._adjacency_matrix.to_numpy(dtype=bool, copy=copy)
    
    def set_adjacency_matrix(self, adjacency_matrix: np.ndarray) -> "Graph":
        if len(adjacency_matrix.shape) != 2:
            raise Exception('adjacency_matrix must be a 2D matrix.')
        if adjacency_matrix.shape[0] != adjacency_matrix.shape[1]:
            raise Exception('adjacency_matrix must be a square matrix.')
        if adjacency_matrix.dtype != bool:
            raise Exception('adjacency_matrix must be a boolean matrix.')
        # Remove edges directions
        adjacency_matrix = np.bitwise_or(adjacency_matrix, adjacency_matrix.T)
        try:
            if self._adjacency_matrix.shape != adjacency_matrix.shape:
                raise Exception('adjacency_matrix must have the same shape of current matrix.')
            else:
                # If the adjacency_matrix is already defined and has the same
                # shape of the new adjacency_matrix, create a new matrix using
                # the new data and keeping the previous node names
                nodes = self.nodes()
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
        del(self[node])
        self._adjacency_matrix.drop(node, axis=0, inplace=True)
        self._adjacency_matrix.drop(node, axis=1, inplace=True)
        return self

    def add_edge(self, parent: str, child: str, undirected: bool = False) -> "Graph":
        if parent not in self._adjacency_matrix or child not in self._adjacency_matrix:
            raise Exception('parent and child nodes must be in adjacency_matrix before adding edge.')
        self._adjacency_matrix.loc[parent, child] = True
        self._adjacency_matrix.loc[child, parent] = True
        return self

    def remove_edge(self, parent: str, child: str) -> "Graph":
        if parent not in self._adjacency_matrix or child not in self._adjacency_matrix:
            raise Exception('parent and child nodes must be in adjacency_matrix before removing edge.')
        self._adjacency_matrix.loc[parent, child] = False
        self._adjacency_matrix.loc[child, parent] = False
        return self
    
    def is_directed(self) -> bool:
        return False

    def __repr__(self):
        return str(self._adjacency_matrix)
    
    def to_networkx(self) -> nx.Graph:
        mapping = {k:v for k,v in enumerate(self.nodes())}
        G = nx.Graph(self.adjacency_matrix())
        G = nx.relabel_nodes(G, mapping)
        attributes = self._nodes_attributes
        for node in self.nodes():
            if node in attributes.keys():
                for key, value in attributes[node].items():
                    G.nodes[node][key] = deepcopy(value)
        return G
    
    def plot(self) -> None:
        G = self.to_networkx()
        nx.draw(G, with_labels=True)
        plt.show()
    
    @classmethod
    def from_networkx(cls, G: nx.Graph) -> "Graph":
        nodes = [str(node) for node in G.nodes]
        adjacent_matrix = nx.to_numpy_array(G).astype(bool)
        return cls(nodes, adjacent_matrix)


class DirectedGraph(Graph):

    def __init__(self, nodes: List[str] = None, adjacency_matrix: np.ndarray = None) -> None:
        super().__init__(nodes, adjacency_matrix)
    
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
                nodes = self.nodes()
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
    
    def add_edge(self, parent: str, child: str) -> "DirectedGraph":
        if parent not in self._adjacency_matrix or child not in self._adjacency_matrix:
            raise Exception('parent and child nodes must be in adjacency_matrix before adding edge.')
        self._adjacency_matrix.loc[parent, child] = True
        return self

    def remove_edge(self, parent: str, child: str) -> "DirectedGraph":
        if parent not in self._adjacency_matrix or child not in self._adjacency_matrix:
            raise Exception('parent and child nodes must be in adjacency_matrix before removing edge.')
        self._adjacency_matrix.loc[parent, child] = False
        return self
    
    def reverse_edge(self, parent: str, child: str) -> "DirectedGraph":
        if parent not in self._adjacency_matrix or child not in self._adjacency_matrix:
            raise Exception('parent and child nodes must be in adjacency_matrix before reversing edge.')
        self._adjacency_matrix.loc[parent, child] = False
        self._adjacency_matrix.loc[child, parent] = True
        return self
        
    def is_directed(self) -> bool:
        return True
    
    def to_undirected(self) -> "Graph":
        return Graph(self.nodes(), self.adjacency_matrix())
    
    def to_networkx(self) -> nx.Graph:
        mapping = {k:v for k,v in enumerate(self.nodes())}
        G = nx.DiGraph(self.adjacency_matrix())
        G = nx.relabel_nodes(G, mapping)
        attributes = self._nodes_attributes
        for node in self.nodes():
            if node in attributes.keys():
                for key, value in attributes[node].items():
                    G.nodes[node][key] = deepcopy(value)
        return G
    
    def plot(self) -> None:
        G = self.to_networkx()
        nx.draw(
            G,
            pos = nx.nx_pydot.graphviz_layout(G, prog='dot'),
            with_labels = True
        )
        plt.show()
    
    @classmethod
    def from_structure(cls, structure: str) -> "DirectedGraph":
        pattern = re.compile(r"\[(\w*)(?:\|(\w+[:\w+]*)){0,1}\]")
        edges = re.findall(pattern, structure)
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
