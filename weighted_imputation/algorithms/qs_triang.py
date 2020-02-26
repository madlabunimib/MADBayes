import numpy as np
from ..structure import Graph, PrefixTree
from typing import List, Set
from queue import Queue


def saturate_set():
    pass

def find_connected_component_of_set(set_nodes: Set, graph: Graph) -> Set:
    adj_matrix = graph.get_adjacency_matrix()
    graph_nodes = graph.get_nodes()
    set_nodes = [graph_nodes.index(node) for node in set_nodes]
    queue = Queue(maxsize = 0) #infinity queue

    node_to_be_visited = set_nodes[:]
    connected_components = []
    while node_to_be_visited != []:
        queue.put(node_to_be_visited[0])
        node_to_be_visited.remove(node_to_be_visited[0])
        connected_component = set()
        while not queue.empty():
            node = queue.get()
            connected_component.add(node)
            for child in _get_neighborhood_in_subset(adj_matrix, node, set_nodes):
                if child in node_to_be_visited:
                    node_to_be_visited.remove(child)
                    queue.put(child)
                    connected_component.add(child)
        connected_components.append(connected_component)
    return connected_components

def bfs(graph: Graph, source_index: int) -> List[Set]:
    adj_matrix = graph.get_adjacency_matrix()
    graph_nodes = graph.get_nodes()
    visited = np.zeros(len(graph_nodes), dtype=bool)
    distances = np.zeros(len(graph_nodes), dtype=int)
    queue = Queue(maxsize = 0) #infinity queue
    
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
                distance_i_from_s.add(elem)
        distance_l_from_s.append(distance_i_from_s)

    return distance_l_from_s

def _get_neighborhood_of_set(adj_matrix: np.ndarray, set_nodes: Set) -> List[int]:
    neighborhood = []
    for node in set_nodes:
        neighborhood.extend(_get_neighborhood(adj_matrix, node))
    return set(neighborhood)

def _get_neighborhood(adj_matrix: np.ndarray, parent_index: int) -> List[int]:
    neighbors = []
    n = adj_matrix.shape[0]
    for index in range(n):
        if adj_matrix[parent_index, index] == 1 or adj_matrix[index, parent_index] == 1:
            neighbors.append(index)
    return neighbors

def _get_neighborhood_in_subset(adj_matrix: np.ndarray, parent_index: int, subset: List) -> List[int]:
    neighbors = []
    n = adj_matrix.shape[0]
    for index in range(n):
        if adj_matrix[parent_index, index] == 1 or adj_matrix[index, parent_index] == 1:
            if index in subset:
                neighbors.append(index)
    return neighbors