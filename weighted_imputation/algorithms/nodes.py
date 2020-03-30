from typing import List
from copy import deepcopy

import numpy as np

from ..backends import AlternativeBackend
from ..structures import Graph, DirectedGraph

def subgraph(graph: Graph, nodes: List[str], attributes: bool = True) -> Graph:
    _nodes = graph.nodes()
    if not set(nodes).issubset(set(_nodes)):
        raise Exception('node not in graph.')
    indices = np.array([_nodes.index(node) for node in nodes])
    adjacency_matrix = graph.adjacency_matrix(copy=False)
    subset = _subset(indices, adjacency_matrix)
    subgraph = type(graph)(nodes, subset)
    if attributes:
        for node in nodes:
            subgraph[node] = deepcopy(graph[node])
    return subgraph

@AlternativeBackend()
def _subset(nodes: np.ndarray, A: np.ndarray) -> np.ndarray:
    return A[nodes, :][:, nodes]

def parents(graph: Graph, node: str) -> List[str]:
    nodes = graph.nodes()
    if not node in nodes:
        raise Exception('node not in graph.')
    adjacency_matrix = graph.adjacency_matrix(copy=False)
    parents = _parents(nodes.index(node), adjacency_matrix)
    parents = [nodes[parent] for parent in parents]
    return parents

@AlternativeBackend()
def _parents(node: int, A: np.ndarray) -> np.ndarray:
    parents = A.T[node]
    parents = np.nonzero(parents)[0].T
    return parents

def family(graph: Graph, node: str) -> List[str]:
    nodes = graph.nodes()
    if not node in nodes:
        raise Exception('node not in graph.')
    adjacency_matrix = graph.adjacency_matrix(copy=False)
    family = _family(nodes.index(node), adjacency_matrix)
    family = [nodes[famil] for famil in family]
    return family

@AlternativeBackend()
def _family(node: int, A: np.ndarray) -> np.ndarray:
    parents = _parents(node, A)
    family = np.append(parents, [node])
    return family

def children(graph: Graph, node: str) -> List[str]:
    nodes = graph.nodes()
    if not node in nodes:
        raise Exception('node not in graph.')
    adjacency_matrix = graph.adjacency_matrix(copy=False)
    children = _children(nodes.index(node), adjacency_matrix)
    children = [nodes[child] for child in children]
    return children

@AlternativeBackend()
def _children(node: int, A: np.ndarray) -> np.ndarray:
    children = A[node]
    children = np.nonzero(children)[0].T
    return children

def neighbors(graph: Graph, node: str) -> List[str]:
    nodes = graph.nodes()
    if not node in nodes:
        raise Exception('node not in graph.')
    adjacency_matrix = graph.adjacency_matrix(copy=False)
    neighbors = _neighbors(nodes.index(node), adjacency_matrix)
    neighbors = [nodes[neighbor] for neighbor in neighbors]
    return neighbors

@AlternativeBackend()
def _neighbors(node: int, A: np.ndarray) -> np.ndarray:
    parents = _parents(node, A)
    children = _children(node, A)
    neighbors = np.append(parents, children)
    neighbors = np.unique(neighbors)
    return neighbors

def boundary(graph: Graph, nodes: List[str]) -> List[str]:
    _nodes = graph.nodes()
    if not set(nodes).issubset(set(_nodes)):
        raise Exception('node not in graph.')
    indices = np.array([_nodes.index(node) for node in nodes])
    adjacency_matrix = graph.adjacency_matrix(copy=False)
    boundary = _boundary(indices, adjacency_matrix)
    boundary = [_nodes[bound] for bound in boundary]
    return boundary

@AlternativeBackend()
def _boundary(nodes: np.ndarray, A: np.ndarray) -> np.ndarray:
    boundary = []
    for node in nodes:
        neighbors = _neighbors(node, A)
        boundary.extend(neighbors)
    boundary = set(boundary).difference(set(nodes))
    boundary = np.array(sorted(boundary))
    return boundary

def ancestors(graph, node: str) -> List[str]:
    nodes = graph.nodes()
    if not node in nodes:
        raise Exception('node not in graph.')
    adjacency_matrix = graph.adjacency_matrix(copy=False)
    ancestors = _ancestors(nodes.index(node), adjacency_matrix)
    ancestors = [nodes[ancestor] for ancestor in ancestors]
    return ancestors

@AlternativeBackend()
def _ancestors(node: int, A: np.ndarray) -> np.ndarray:
    parents = _parents(node, A)
    ancestors = _ancestors_recursive(parents, A)
    return ancestors

def _ancestors_recursive(nodes: np.ndarray, A: np.ndarray) -> np.ndarray:
    ancestors = set(nodes)
    for node in nodes:
        parents = _parents(node, A)
        ancestors = ancestors.union(
            set(_ancestors_recursive(parents, A))
        )
    ancestors = np.array(list(ancestors))
    return ancestors

def descendants(graph, node: str) -> List[str]:
    nodes = graph.nodes()
    if not node in nodes:
        raise Exception('node not in graph.')
    adjacency_matrix = graph.adjacency_matrix(copy=False)
    descendants = _descendants(nodes.index(node), adjacency_matrix)
    descendants = [nodes[descendant] for descendant in descendants]
    return descendants

@AlternativeBackend()
def _descendants(node: int, A: np.ndarray) -> np.ndarray:
    children = _children(node, A)
    descendants = _descendants_recursive(children, A)
    return descendants

def _descendants_recursive(nodes: np.ndarray, A: np.ndarray) -> np.ndarray:
    descendants = set(nodes)
    for node in nodes:
        children = _children(node, A)
        descendants = descendants.union(
            set(_descendants_recursive(children, A))
        )
    descendants = np.array(list(descendants))
    return descendants

def numbering(graph: Graph) -> np.ndarray:
    nodes = graph.nodes()
    nodes = np.array(nodes)
    numbering = _numbering(nodes)
    return numbering

@AlternativeBackend()
def _numbering(nodes: np.ndarray) -> np.ndarray:
    numbering = np.array(nodes, copy=True)
    return numbering

def perfect_numbering(graph: Graph) -> List[str]:
    nodes = graph.nodes()
    adjacency_matrix = graph.adjacency_matrix(copy=False)
    numbering = _perfect_numbering(0, adjacency_matrix)
    numbering = [nodes[number] for number in numbering]
    return numbering

# TODO: Refactor this function using OrderedSet
@AlternativeBackend()
def _perfect_numbering(node: int, A: np.ndarray) -> np.ndarray:
    n = A.shape[0]
    X = set(range(n))
    numbering = set()
    numbering.add(node)
    neighbors = {i: set(_neighbors(i, A)) for i in range(n)}
    while len(X) > 0:
        X = X.difference(numbering)
        xmax = {key: neighbors[key] for key in X}
        xmax = {key: value.difference(numbering) for key, value in xmax.items()}
        xmax = {key: len(value) for key, value in xmax.items()}
        xmax = max(xmax, key=xmax.get)
        numbering.add(xmax)
    return numbering

def is_complete(graph: Graph) -> bool:
    adjacency_matrix = graph.adjacency_matrix(copy=False)
    is_complete = _is_complete(adjacency_matrix)
    return is_complete

@AlternativeBackend()
def _is_complete(A: np.ndarray) -> bool:
    out = A.copy()
    np.fill_diagonal(out, True)
    return out.all()

@AlternativeBackend()
def _is_complete_set(nodes: np.ndarray, A: np.ndarray) -> bool:
    out = _subset(nodes, A)
    return _is_complete(out)

@AlternativeBackend()
def _fill_in(A: np.array) -> np.ndarray:
    out = A.copy()
    np.fill_diagonal(out, True)
    np.bitwise_not(out, out)
    indices = np.argwhere(out)
    return indices

@AlternativeBackend()
def _fill_in_set(nodes: np.ndarray, A: np.array) -> np.ndarray:
    out = _subset(nodes, A)
    indices = _fill_in(out)
    # Convert relative indices to absolute indices
    n = indices.shape[0]
    for i in range(n):
        indices[i, 0] = nodes[indices[i, 0]]
        indices[i, 1] = nodes[indices[i, 1]]
    return indices

@AlternativeBackend()
def _filter(nodes: np.ndarray, A: np.ndarray) -> np.ndarray:
    out = A.copy()
    out[:] = False
    n = len(nodes)
    for i in range(n):
        out[nodes[i]] = A[nodes[i]]
    return out
