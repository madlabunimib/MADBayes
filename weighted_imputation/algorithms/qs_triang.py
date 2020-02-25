import numpy as np
from ..structure import Graph, PrefixTree
from typing import List, Set
from queue import Queue 


def bfs(graph: Graph, s: int) -> List[Set]:
    adj_matrix = graph.get_adjacency_matrix()
    graph_nodes = graph.get_nodes()
    visited = np.zeros(len(graph_nodes), dtype=bool)
    distances = np.zeros(len(graph_nodes), dtype=int)
    queue = Queue(maxsize = 0) #infinity queue
    
    source_index = graph_nodes.index(s)
    queue.put(source_index)
    visited[source_index] = True
    while not queue.empty():
        node = queue.get()
        for child in _get_neighborhood(adj_matrix, node):
            if visited[child] == False:
                visited[child] = True
                distances[child] = distances[node] + 1
                queue.put(child)

    distance_l_from_s = []
    for distance in range(max(distances)+1):
        distance_i_from_s = set()
        for elem in range(len(graph_nodes)):
            if distances[elem] == distance:
                distance_i_from_s.add(graph.get_nodes()[elem])
        distance_l_from_s.append(distance_i_from_s)

    return distance_l_from_s

def _get_neighborhood(adj_matrix: np.ndarray, parent_index: int) -> List[int]:
    neighbors = []
    n = adj_matrix.shape[0]
    for index in range(n):
        if adj_matrix[parent_index, index] == 1 or adj_matrix[index, parent_index] == 1:
            neighbors.append(index)
    return neighbors