import numpy as np
from numba import njit
from numba.typed import Dict
from .nodes import _neighbors, _fill_in_set, _filter
from .paths import _all_simple_paths
from ..structures import Graph
from ..utils import union, intersection, difference

def MCS(graph: Graph, return_new_edges: bool = False) -> np.ndarray:
    if not isinstance(graph, Graph):
        raise Exception('graph must be istance of Graph class.')
    adjacency_matrix = graph.get_adjacency_matrix()
    new_edges = np.zeros(adjacency_matrix.shape, dtype=bool)
    _MCS(0, adjacency_matrix, new_edges)
    triangulated = Graph(graph.get_nodes(), adjacency_matrix)
    if return_new_edges:
        return triangulated, new_edges
    return triangulated

@njit(cache=True)
def _MCS(node: int, A: np.ndarray, out: np.ndarray) -> np.ndarray:
    i = 1
    n = A.shape[0]
    while i < n:
        if i == 1:
            numbering = np.array([node])
            X = np.array([i for i in range(n)])
            # Caching neighbors
            neighbors = Dict()
            for j in range(n):
                neighbors[X[j]] = _neighbors(X[j], A)
        i += 1
        X = difference(X, numbering)
        x = X.shape[0]
        vmax = -1
        pmax = -1
        for j in range(x):
            k = len(intersection(neighbors[X[j]], numbering))
            if vmax < k:
                vmax = k
                pmax = j
        numbering = np.append(numbering, [X[pmax]])
        nodes = intersection(neighbors[X[pmax]], numbering[:i])
        if _add_missing_edges(nodes, A, out):
            i = 1

@njit(cache=True)
def _add_missing_edges(nodes: np.ndarray, A: np.ndarray, out: np.ndarray) -> bool:
    indices = _fill_in_set(nodes, A)
    n = indices.shape[0]
    if n > 0:
        for i in range(n):
            out[indices[i, 0], indices[i, 1]] = True
        np.bitwise_or(out, A, A)
        return True
    return False

def MCS_M(graph: Graph, return_new_edges: bool = False) -> np.ndarray:
    if not isinstance(graph, Graph):
        raise Exception('graph must be istance of Graph class.')
    adjacency_matrix = graph.get_adjacency_matrix()
    n = adjacency_matrix.shape[0]
    weights = np.zeros(n, dtype=int)
    new_edges = np.zeros((n, n), dtype=bool)
    _MCS_M(adjacency_matrix, weights, new_edges)
    triangulated = Graph(graph.get_nodes(), adjacency_matrix)
    if return_new_edges:
        return triangulated, new_edges
    return triangulated

@njit(cache=True)
def _MCS_M(
        A: np.ndarray,
        weights: np.ndarray,
        out: np.ndarray
    ) -> np.ndarray:
    n = A.shape[0]
    for i in range(n):
        # Choose an unnumbered vertex z of maximum weights
        z = np.argmax(weights)
        # Select the unnumbered vertexes
        unnumbered = np.nonzero(weights > -1)[0]
        # Check all paths of unnumbered vertices between y and z
        m = unnumbered.shape[0]
        for j in range(m):
            y = unnumbered[j]
            if y != z:
                # Limit the research in the subgraph of unnumbered vertices
                subgraph = _filter(unnumbered, A)
                # Check if exists a path y-...-xi-...-z where weights[xi] < weights[y]
                exists = _MCS_M_check_paths(y, z, subgraph, weights)
                if exists:
                    # Update the weights
                    weights[y] = weights[y] + 1
                    # Add the y-z edge to the minimal fill-in set
                    out[y, z] = True
        # Set z as numbered by setting its weight to -1
        weights[z] = -1
    # Add minimal fill-in to current graph
    np.bitwise_or(out, out.T, out)
    np.bitwise_or(out, A, A)

@njit(cache=True)
def _MCS_M_check_paths(source: int, target: int, A: np.ndarray, weigths: np.ndarray) -> bool:
    paths = _all_simple_paths(source, target, A)
    for path in paths:
        exists = True
        for node in path:
            if weigths[node] >= weigths[source] and node != target:
                exists = False
        if exists:
            return True
    return False
