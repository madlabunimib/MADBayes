import numpy as np

from ..backends import alternative_backend


@alternative_backend()
def _subset(nodes: np.ndarray, A: np.ndarray) -> np.ndarray:
    return A[nodes, :][:, nodes]

@alternative_backend()
def _parents(node: int, A: np.ndarray) -> np.ndarray:
    parents = A.T[node]
    parents = np.nonzero(parents)[0].T
    return parents

@alternative_backend()
def _family(node: int, A: np.ndarray) -> np.ndarray:
    parents = _parents(node, A)
    family = np.append(parents, [node])
    return family

@alternative_backend()
def _children(node: int, A: np.ndarray) -> np.ndarray:
    children = A[node]
    children = np.nonzero(children)[0].T
    return children

@alternative_backend()
def _neighbors(node: int, A: np.ndarray) -> np.ndarray:
    parents = _parents(node, A)
    children = _children(node, A)
    neighbors = np.append(parents, children)
    neighbors = np.unique(neighbors)
    return neighbors

@alternative_backend()
def _boundary(nodes: np.ndarray, A: np.ndarray) -> np.ndarray:
    boundary = []
    for node in nodes:
        neighbors = _neighbors(node, A)
        boundary.extend(neighbors)
    boundary = set(boundary).difference(set(nodes))
    boundary = np.array(sorted(boundary))
    return boundary

@alternative_backend()
def _ancestors(node: int, A: np.ndarray) -> np.ndarray:
    parents = _parents(node, A)
    ancestors = _ancestors_recursive(parents, A)
    return ancestors

@alternative_backend()
def _ancestors_recursive(nodes: np.ndarray, A: np.ndarray) -> np.ndarray:
    ancestors = set(nodes)
    for node in nodes:
        parents = _parents(node, A)
        ancestors = ancestors.union(
            set(_ancestors_recursive(parents, A))
        )
    ancestors = np.array(list(ancestors))
    return ancestors

@alternative_backend()
def _descendants(node: int, A: np.ndarray) -> np.ndarray:
    children = _children(node, A)
    descendants = _descendants_recursive(children, A)
    return descendants

@alternative_backend()
def _descendants_recursive(nodes: np.ndarray, A: np.ndarray) -> np.ndarray:
    descendants = set(nodes)
    for node in nodes:
        children = _children(node, A)
        descendants = descendants.union(
            set(_descendants_recursive(children, A))
        )
    descendants = np.array(list(descendants))
    return descendants

@alternative_backend()
def _numbering(nodes: np.ndarray) -> np.ndarray:
    numbering = np.array(nodes, copy=True)
    return numbering

@alternative_backend()
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
        xmax = max(xmax, key=max.get)
        numbering.add(xmax)
    return numbering

@alternative_backend()
def _is_complete(A: np.ndarray) -> bool:
    out = A.copy()
    np.fill_diagonal(out, True)
    return out.all()

@alternative_backend()
def _is_complete_set(nodes: np.ndarray, A: np.ndarray) -> bool:
    out = _subset(nodes, A)
    return _is_complete(out)

@alternative_backend()
def _fill_in(A: np.array) -> np.ndarray:
    out = A.copy()
    np.fill_diagonal(out, True)
    np.bitwise_not(out, out)
    indices = np.argwhere(out)
    return indices

@alternative_backend()
def _fill_in_set(nodes: np.ndarray, A: np.array) -> np.ndarray:
    out = _subset(nodes, A)
    indices = _fill_in(out)
    # Convert relative indices to absolute indices
    n = indices.shape[0]
    for i in range(n):
        indices[i, 0] = nodes[indices[i, 0]]
        indices[i, 1] = nodes[indices[i, 1]]
    return indices

@alternative_backend()
def _filter(nodes: np.ndarray, A: np.ndarray) -> np.ndarray:
    out = A.copy()
    out[:] = False
    n = len(nodes)
    for i in range(n):
        out[nodes[i]] = A[nodes[i]]
    return out
