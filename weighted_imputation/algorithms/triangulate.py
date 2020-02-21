import numpy as np
from ..structure import Graph, PrefixTree
from ..utils import plot_graph, plot_prefix_tree
from typing import List


def triangulate(graph: Graph) -> Graph:

    #TEST STRING "[1][8][2|1:8][5|1][6|5][3|2][4|2][7|3:4:6]"
    #TEST STRING ESTESA "[1][8|9][2|1:8:10][5|1][6|5][3|2][4|2][7|3:4:6]"
    
    A = graph.get_adjacency_matrix()    
    out = np.zeros(A.shape, dtype=bool)
    new_edges = []

    print("nodes:")
    print(graph.get_nodes())
    _moralize(A, out, new_edges)

    print("new edges: ")
    print(new_edges)

    #search for cycles with lenght >3
    for elem in new_edges:
        print("########################################")
        print(_find_cycle(A, elem[0], elem[1]))


    return



def _break_cycle(cycle: List) -> List:
    new_archs = []
    master_node = cycle[0]
    cycle = cycle[2:-2]

    for node in cycle:
        new_archs.append((master_node, node))


    return new_archs

def _find_cycle(adj_matrix: np.ndarray, node_0: int, node_1: int) -> list:

    n = adj_matrix.shape[0]
    prefix_tree = PrefixTree([], np.zeros(shape=(0,0)))

    #prefix_tree = _build_tree(node_0, prefix_tree, False, adj_matrix)
    #prefix_tree = _build_tree(node_1, prefix_tree, True, adj_matrix)

    #Costruzione prefix tree partendo dal primo nodo
    prefix_tree.add_node(node_0)
    leafs = [node_0]
    while leafs != []:
        new_leafs = []
        old_leafs = set()
        for leaf in leafs:
            for row in range(n):
                if adj_matrix[row, leaf] == 1:
                    prefix_tree.add_node(row)
                    prefix_tree.add_edge(row, leaf)
                    new_leafs.append(row)
            old_leafs.add(leaf)
        leafs = [x for x in leafs if not x in old_leafs]
        leafs.extend(new_leafs)

    #Costruzione prefix tree partendo dal secondo nodo
    prefix_tree.add_node(node_1)
    leafs = [node_1]
    while leafs != []:
        new_leafs = []
        old_leafs = set()
        for leaf in leafs:
            for row in range(n):
                if adj_matrix[row, leaf] == 1:
                    #Trovato il nodo in comune costruisco il ciclo e lo ritorno senza continuare la costruzione
                    if row in prefix_tree.get_nodes():
                        prefix_tree.add_node(row)
                        prefix_tree.add_edge(row, leaf)
                        new_leafs.append(row)
                        return _build_cycle_path(prefix_tree, row)

                    prefix_tree.add_node(row)
                    prefix_tree.add_edge(row, leaf)
                    new_leafs.append(row)              
            old_leafs.add(leaf)
        leafs = [x for x in leafs if not x in old_leafs]
        leafs.extend(new_leafs)
            
    return []


def _build_cycle_path(prefix_tree: PrefixTree, root: int) -> List:
    
    adj_matrix = prefix_tree.get_adjacency_matrix() 
    n = adj_matrix.shape[0]
    root = prefix_tree.get_nodes().index(root)

    childs = ['','']
    first_part = [root]
    second_part = [root]

    while first_part[-1] != '$' and second_part[-1] != '$':
        childs[0] = '$'
        childs[1] = '$'
        for row in range(n):
            if adj_matrix[first_part[-1], row] == 1:
                childs[0] = row
            if adj_matrix[second_part[-1], row] == 1:
                childs[1] = row       
        first_part.append(childs[0])
        second_part.append(childs[1])

    
    cycles = first_part[:-1] #Metto la prima parte togliendo il terminatore $
    second_part.reverse() 
    cycles.extend(second_part[1:]) #Concateno la seconda parte togliendo il terminatore $
    # Mappo dagli indici del prefix tree agli indici del grafo da triangolare
    return [prefix_tree.get_nodes()[node] for node in cycles]  
       

def _build_tree(start_node: int, prefix_tree: PrefixTree, early_stop: bool, adj_matrix: np.ndarray):    
    n = adj_matrix.shape[0]
    
    prefix_tree.add_node(start_node)
    leafs = [start_node]
    while leafs != []:
        new_leafs = []
        old_leafs = set()
        for leaf in leafs:
            for row in range(n):
                if adj_matrix[row, leaf] == 1:
                    if early_stop and row in prefix_tree.get_nodes():
                        print(row)
                    else:
                        prefix_tree.add_node(row)
                        prefix_tree.add_edge(row, leaf)
                        new_leafs.append(row)
            old_leafs.add(leaf)
        leafs = [x for x in leafs if not x in old_leafs]
        leafs.extend(new_leafs)
    return prefix_tree


def _moralize(A, out,new_edges: List):
       
    n = A.shape[0]
    for columns in range(n):
        parents = A.T[columns]
        indexes = np.nonzero(parents)[0].T
        for i in indexes:
            for j in indexes:
                if i != j:
                    out[i, j] = True
                    if i < j:
                        new_edges.append((i,j))
    np.bitwise_or(A, out, out)
    np.bitwise_or(out, out.T, out)
