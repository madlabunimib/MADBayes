import re
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from copy import deepcopy
from typing import List, Dict
from ..algorithms import _subset, _parents, _family, _children, _neighbors, _boundary
from ..algorithms import _ancestors, _descendants, _numbering, _is_complete


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
        return len(self.get_nodes())

    def __getitem__(self, key) -> Dict:
        if not key in self.get_nodes():
            raise KeyError('node not in graph.')
        if not key in self._nodes_attributes.keys():
            self._nodes_attributes[key] = {}
        return self._nodes_attributes[key]

    def __setitem__(self, key, value) -> None:
        if not key in self.get_nodes():
            raise KeyError('node not in graph.')
        self._nodes_attributes[key] = value

    def __delitem__(self, key) -> None:
        del(self._nodes_attributes[key])

    def __iter__(self):
        return self._nodes_attributes.iteritems()

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
            # Remapping nodes attributes
            self._nodes_attributes = {
                key: self._nodes_attributes[value]
                for key, value in mapping
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

    def get_adjacency_matrix(self, copy: bool = True) -> np.ndarray:
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
        del(self._nodes_attributes[node])
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
    
    def subgraph(self, nodes: List[str]) -> np.ndarray:
        _nodes = self.get_nodes()
        if not set(nodes).issubset(set(_nodes)):
            raise Exception('node not in graph.')
        indices = np.array([_nodes.index(node) for node in nodes])
        adjacency_matrix = self.get_adjacency_matrix(copy=False)
        subset = _subset(indices, adjacency_matrix)
        subgraph = Graph(nodes, subset)
        for node in nodes:
            subgraph[node] = deepcopy(self[node])
        return subgraph
    
    def neighbors(self, node: str) -> np.ndarray:
        nodes = self.get_nodes()
        if not node in nodes:
            raise Exception('node not in graph.')
        adjacency_matrix = self.get_adjacency_matrix(copy=False)
        neighbors = _neighbors(nodes.index(node), adjacency_matrix)
        neighbors = [nodes[neighbor] for neighbor in neighbors]
        return neighbors
    
    def boundary(self, nodes: List[str]) -> np.ndarray:
        _nodes = self.get_nodes()
        if not set(nodes).issubset(set(_nodes)):
            raise Exception('node not in graph.')
        indices = np.array([_nodes.index(node) for node in nodes])
        adjacency_matrix = self.get_adjacency_matrix(copy=False)
        boundary = _boundary(indices, adjacency_matrix)
        boundary = [_nodes[bound] for bound in boundary]
        return boundary
    
    def numbering(self) -> np.ndarray:
        nodes = self.get_nodes()
        nodes = np.array(nodes)
        numbering = _numbering(nodes)
        return numbering
    
    def is_complete(self) -> bool:
        adjacency_matrix = self.get_adjacency_matrix(copy=False)
        is_complete = _is_complete(adjacency_matrix)
        return is_complete
    
    def is_directed(self) -> bool:
        return False

    def __repr__(self):
        return str(self._adjacency_matrix)
    
    def to_networkx(self) -> nx.Graph:
        mapping = {k:v for k,v in enumerate(self.get_nodes())}
        G = nx.Graph(self.get_adjacency_matrix())
        G = nx.relabel_nodes(G, mapping)
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
    
    def add_edge(self, parent: str, child: str, undirected: bool = False) -> "DirectedGraph":
        if parent not in self._adjacency_matrix or child not in self._adjacency_matrix:
            raise Exception('parent and child nodes must be in adjacency_matrix before adding edge.')
        self._adjacency_matrix.loc[parent, child] = True
        return self

    def remove_edge(self, parent: str, child: str) -> "DirectedGraph":
        if parent not in self._adjacency_matrix or child not in self._adjacency_matrix:
            raise Exception('parent and child nodes must be in adjacency_matrix before removing edge.')
        self._adjacency_matrix.loc[parent, child] = False
        return self
    
    def subgraph(self, nodes: List[str]) -> np.ndarray:
        _nodes = self.get_nodes()
        if not set(nodes).issubset(set(_nodes)):
            raise Exception('node not in graph.')
        indices = np.array([_nodes.index(node) for node in nodes])
        adjacency_matrix = self.get_adjacency_matrix(copy=False)
        subset = _subset(indices, adjacency_matrix)
        subgraph = DirectedGraph(nodes, subset)
        for node in nodes:
            subgraph[node] = deepcopy(self[node])
        return subgraph

    def parents(self, node: str) -> np.ndarray:
        nodes = self.get_nodes()
        if not node in nodes:
            raise Exception('node not in graph.')
        adjacency_matrix = self.get_adjacency_matrix(copy=False)
        parents = _parents(nodes.index(node), adjacency_matrix)
        parents = [nodes[parent] for parent in parents]
        return parents

    def family(self, node: str) -> np.ndarray:
        nodes = self.get_nodes()
        if not node in nodes:
            raise Exception('node not in graph.')
        adjacency_matrix = self.get_adjacency_matrix(copy=False)
        family = _family(nodes.index(node), adjacency_matrix)
        family = [nodes[famil] for famil in family]
        return family

    def children(self, node: str) -> np.ndarray:
        nodes = self.get_nodes()
        if not node in nodes:
            raise Exception('node not in graph.')
        adjacency_matrix = self.get_adjacency_matrix(copy=False)
        children = _children(nodes.index(node), adjacency_matrix)
        children = [nodes[child] for child in children]
        return children
    
    def ancestors(self, node: str) -> np.ndarray:
        nodes = self.get_nodes()
        if not node in nodes:
            raise Exception('node not in graph.')
        adjacency_matrix = self.get_adjacency_matrix(copy=False)
        ancestors = _ancestors(nodes.index(node), adjacency_matrix)
        ancestors = [nodes[ancestor] for ancestor in ancestors]
        return ancestors
    
    def descendants(self, node: str) -> np.ndarray:
        nodes = self.get_nodes()
        if not node in nodes:
            raise Exception('node not in graph.')
        adjacency_matrix = self.get_adjacency_matrix(copy=False)
        descendants = _descendants(nodes.index(node), adjacency_matrix)
        descendants = [nodes[descendant] for descendant in descendants]
        return descendants
    
    def is_directed(self):
        return True
    
    def to_undirected(self) -> "Graph":
        return Graph(self.get_nodes(), self.get_adjacency_matrix())
    
    def to_networkx(self) -> nx.Graph:
        mapping = {k:v for k,v in enumerate(self.get_nodes())}
        G = nx.DiGraph(self.get_adjacency_matrix())
        G = nx.relabel_nodes(G, mapping)
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
    def from_string(cls, string: str) -> "DirectedGraph":
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
