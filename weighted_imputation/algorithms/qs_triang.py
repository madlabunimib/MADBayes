import numpy as np
from ..structure import Graph, PrefixTree
from ..utils import plot_graph
from typing import List, Set, Dict
from queue import Queue


def triangulate_graph(graph: Graph) -> Graph:
    quasi_split_graph_dict = find_quasi_split_graph(graph)

    edges_to_add = []
    for elem in quasi_split_graph_dict:
        edges_to_add.extend(min_qs(elem))

    for edge in edges_to_add:
        graph.add_edge(edge[0], edge[1])

    plot_graph(graph)
    return graph

#Return the list of edges to triangulate the quasi-split graph
def min_qs(quasi_split_graph_dict: Dict) -> List:
    adj_matrix = quasi_split_graph_dict["quasi_split_graph"].get_adjacency_matrix()
    nodes = quasi_split_graph_dict["quasi_split_graph"].get_nodes()
    Q = {nodes.index(node) for node in quasi_split_graph_dict["Q"]}
    P = {nodes.index(node) for node in quasi_split_graph_dict["P"]}

    neighborhood_in_p = []
    for v in Q:
        neighborhood_in_p.append((v, len(_get_neighborhood(adj_matrix, v) & P)))
    Q = {elem[0] for elem in sorted(neighborhood_in_p, key=lambda tup: tup[1])}

    D = []
    while Q != set():
        v = Q.pop()
        D.extend(saturate_set(_get_neighborhood(adj_matrix, v)))
        for row in range(adj_matrix.shape[0]):
            adj_matrix[v, row] = False
            adj_matrix[row, v] = False

    return [(nodes[node[0]], nodes[node[1]]) for node in D] 

# Q = node of the connected component 
# P = neighborhood of Q
# F = set of edges needed for saturation
def find_quasi_split_graph(graph: Graph) -> Dict:
    quasi_split_graph_list = []
    #For each node compute the distance from a (random) source node whit BFS 
    set_at_distance_l_from_s = bfs(graph, 0) # 0 is for the first node in the set, it is a random choice
    set_at_distance_l_from_s.reverse()    

    for level in range(len(set_at_distance_l_from_s)-1):
        #Find the connected component for each level
        connencted_components_level = find_connected_component_of_set(graph, set_at_distance_l_from_s[level])
        F = []

        for Q in connencted_components_level:
            #Find the neighborhood of the connected component
            P = _get_neighborhood_of_set_in_subset(
                graph.get_adjacency_matrix(),
                Q,
                set_at_distance_l_from_s[level+1])
            #Saturate the neighborhood
            F_part = saturate_set(P)   
            F.extend(F_part)       
            #Create the quasi-split graph
            nodes = Q | P
            nodes = [graph.get_nodes()[node_index] for node_index in nodes]
            adj_matrix = np.zeros(shape=(len(nodes), len(nodes)), dtype=bool)
            #Add to the quasi-split graph the edges already in the graph
            for i in range(len(adj_matrix)):
                for j in range(len(adj_matrix)):
                    node_i = nodes[i]
                    node_j = nodes[j]
                    if graph.get_adjacency_matrix()[graph.get_nodes().index(node_i),graph.get_nodes().index(node_j)] == True:
                        adj_matrix[i,j] = True        
            #Add to the quasi-split graph the edges add for the saturation
            for edge in F_part:
                edge_0 = graph.get_nodes()[edge[0]]
                edge_1 = graph.get_nodes()[edge[1]]
                adj_matrix[nodes.index(edge_0), nodes.index(edge_1)] = True
            #Create the graph and add to the quasi-split graph list
            quasi_split_graph = Graph(nodes, adj_matrix)
            quasi_split_graph_list.append({
                "quasi_split_graph": quasi_split_graph,
                "P": [graph.get_nodes()[node_index] for node_index in P],
                "Q": [graph.get_nodes()[node_index] for node_index in Q]
                })

        #Add the saturation edges at the graph
        for edge in F:
            graph.add_edge(graph.get_nodes()[edge[0]], graph.get_nodes()[edge[1]])
            graph.add_edge(graph.get_nodes()[edge[1]], graph.get_nodes()[edge[0]])

    return quasi_split_graph_list

def saturate_set(set_nodes: Set) -> List:
    edges_to_add = []
    for node1 in set_nodes:
        for node2 in set_nodes:
            if node1 != node2:
                edges_to_add.append((node1, node2))
    return edges_to_add

def find_connected_component_of_set(graph: Graph, set_nodes: Set) -> Set:
    adj_matrix = graph.get_adjacency_matrix()
    queue = Queue(maxsize = 0) #infinity queue

    node_to_be_visited = [node for node in set_nodes]
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

def _get_neighborhood_of_set(adj_matrix: np.ndarray, set_nodes: Set) -> Set:
    neighborhood = []
    for node in set_nodes:
        neighborhood.extend(_get_neighborhood(adj_matrix, node))
    return set(neighborhood)

def _get_neighborhood_of_set_in_subset(adj_matrix: np.ndarray, set_nodes: Set, subset: List) -> Set:
    neighborhood = []
    for node in set_nodes:
        neighborhood.extend(_get_neighborhood_in_subset(adj_matrix, node, subset))
    return set(neighborhood)

def _get_neighborhood(adj_matrix: np.ndarray, parent_index: int) -> Set:
    neighbors = set()
    n = adj_matrix.shape[0]
    for index in range(n):
        if adj_matrix[parent_index, index] == 1 or adj_matrix[index, parent_index] == 1:
            neighbors.add(index)
    return neighbors

def _get_neighborhood_in_subset(adj_matrix: np.ndarray, parent_index: int, subset: List) -> Set:
    return [node for node in _get_neighborhood(adj_matrix, parent_index) if node in subset]
    