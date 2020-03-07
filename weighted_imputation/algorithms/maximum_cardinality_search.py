import numpy as np
from numba import njit
from numba.typed import Dict
from .depth_first_search import _DFS_Visit
from .nodes import _neighbors, _fill_in_set, _filter
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
    color = np.ones(n, dtype=bool)
    times = -np.ones((n, 2), dtype=int)
    parents = -np.ones(n, dtype=int)
    weights = np.zeros(n, dtype=int)
    new_edges = np.zeros((n, n), dtype=bool)
    _MCS_M(adjacency_matrix, color, times, parents, weights, new_edges)
    triangulated = Graph(graph.get_nodes(), adjacency_matrix)
    if return_new_edges:
        return triangulated, new_edges
    return triangulated

@njit(cache=True)
def _MCS_M(
        A: np.ndarray,
        color: np.ndarray,
        times: np.ndarray,
        parents: np.ndarray,
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
        m = len(unnumbered)
        for j in range(m):
            y = unnumbered[j]
            if y != z:
                # Limit the research in the subgraph of unnumbered vertices
                unnumbered_subgraph = _filter(unnumbered, A)
                # Initialize support variables for DFS on z
                z_color = color.copy()
                z_times = times.copy()
                z_parents = parents.copy()
                # Execute DFS on y
                _DFS_Visit(y, 0, unnumbered_subgraph, z_color, z_times, z_parents)
                raise NotImplementedError('TODO: Check for ALL paths y-z')
                # Check if exists a path y-...-xi-...-z where weights[xi] < weights[y]
                exists = True
                parent = z_parents[y]
                while exists and parent != z:
                    if parent == -1 or weights[parent] >= weights[y]:
                        exists = False
                    else:
                        parent = z_parents[parent]
                if exists:
                    # Update the weights
                    weights[y] = weights[y] + 1
                    # Add the y-z edge to the minimal fill-in set
                    out[y, z] = True
                    out[z, y] = True
        # Set z as numbered by setting its weight to -1
        weights[z] = -1
    # Add minimal fill-in to current graph
    np.bitwise_or(out, A, A)
