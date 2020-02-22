import numpy as np
from ..structure import Graph, PrefixTree
from ..utils import plot_graph, plot_prefix_tree
from typing import List, Dict


def triangulate(graph: Graph, moralized_graph: Graph, new_edges: np.ndarray) -> Graph:
    original_adj_matrix = graph.get_adjacency_matrix()
    adj_matrix = moralized_graph.get_adjacency_matrix()
    n = new_edges.shape[0]
    new_edges = [
        (i,j) 
        for i in range(n) 
        for j in range(n) 
        if new_edges[i,j] == True]
    
    #search for cycles with lenght >3
    cycles_list = []
    for elem in new_edges:
        #We use the adj_matrix before moralization to take advantage of the oriented edges
        cycles_list.append(_find_cycle(original_adj_matrix, elem[0], elem[1]))
        
    #Triangolate cycles and add the new archs to the moralized adj_matrix
        for cycles in cycles_list:
            for cycle in cycles:
                if len(cycle) > 4:
                    edges_to_add = _break_cycle(cycle)
                    for edge in edges_to_add:
                        if edge[0] != edge[1]:
                            adj_matrix[edge[0], edge[1]] = True
                            adj_matrix[edge[1], edge[0]] = True

    return Graph(graph.get_nodes(), adj_matrix)

def _find_cycle(adj_matrix: np.ndarray, node_0: int, node_1: int) -> list:
    #Create empty PrefixTree
    prefix_tree = PrefixTree([], np.zeros(shape=(0,0)))
    visited_node = {"first_tree": set(), "second_tree": set()}
    #Insert first path from first node of the new edge
    _build_tree(node_0, prefix_tree, adj_matrix, visited_node, True)
    #Insert second path from second node of the new edge
    _build_tree(node_1, prefix_tree, adj_matrix, visited_node, False)
    cycles = []
    for node_1 in visited_node["first_tree"]:
        for node_2 in visited_node["second_tree"]:
            if node_1 == node_2:
                cycles.append(_build_cycle_path(prefix_tree, node_1))
        
    return cycles

def _build_tree(start_node: int, prefix_tree: PrefixTree, adj_matrix: np.ndarray, visited_node: Dict, first_tree: bool) -> List:    
    n = adj_matrix.shape[0]

    prefix_tree.add_node(start_node)
    leafs = [start_node]
    if first_tree:
        visited_node["first_tree"].add(start_node)
    else:
        visited_node["second_tree"].add(start_node)
    
    while leafs != []:
        new_leafs = []
        old_leafs = set()
        for leaf in leafs:
            for row in range(n):
                if adj_matrix[row, leaf] == 1:
                    prefix_tree.add_node(row)
                    prefix_tree.add_edge(row, leaf)
                    new_leafs.append(row)
                    if first_tree:
                        visited_node["first_tree"].add(row)
                    else:
                        visited_node["second_tree"].add(row)

            old_leafs.add(leaf)
        leafs = [x for x in leafs if not x in old_leafs]
        leafs.extend(new_leafs)
    return []

def _build_cycle_path(prefix_tree: PrefixTree, root: int) -> List:
    adj_matrix = prefix_tree.get_adjacency_matrix()
    n = adj_matrix.shape[0]
    root = prefix_tree.get_nodes().index(root)

    for row in range(n):
        if adj_matrix[root, row] == 1:
            child = row
            break

    first_part = [root, child]
    second_part = [root]
    childs = ['', '']
    while not (first_part[-1] == '$' and second_part[-1] == '$'):
        childs[0] = '$'
        childs[1] = '$'
        for row in range(n):
            if first_part[-1] != '$' and adj_matrix[first_part[-1], row] == 1:
                childs[0] = row
            if second_part[-1] != '$' and adj_matrix[second_part[-1], row] == 1:
                childs[1] = row
        if first_part[-1] != '$':
            first_part.append(childs[0])
        if second_part[-1] != '$':
            second_part.append(childs[1])

    cycles = first_part[:-1] #Metto la prima parte togliendo il terminatore $
    second_part.reverse()
    cycles.extend(second_part[1:]) #Concateno la seconda parte togliendo il terminatore $
    # Mappo dagli indici del prefix tree agli indici del grafo da triangolare
    return [prefix_tree.get_nodes()[node] for node in cycles]

def _break_cycle(cycle: List) -> List:
    new_archs = []
    master_node = cycle[0]
    cycle = cycle[2:-2] #Remove the master node and the adjacent nodes
    for node in cycle:
        new_archs.append((master_node, node))
    return new_archs
