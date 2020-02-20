import numpy as np
from ..structure import Graph
from ..utils import plot_graph
from typing import List


def triangulate(graph: Graph) -> Graph:

    #TEST STRING "[1][8][2|1:8][5|1][6|5][3|2][4|2][7|3:4:6]"
    #TEST STRING ESTESA "[1][8|9][2|1:8:10][5|1][6|5][3|2][4|2][7|3:4:6]"
    
    A = graph.get_adjacency_matrix()    
    out = np.zeros(A.shape, dtype=bool)
    new_edges = []

    #plot original graph
    #plot_graph(graph)
    print("nodes:")
    print(graph.get_nodes())
    _moralize(A, out, new_edges)

    #plot moralized graph and list with add edge(s)
    print("new edges: ")
    print(new_edges)
    #plot_graph(Graph(graph.get_nodes(), out))

    cycles = []
    #search for cycles with lenght >3
    for elem in new_edges:       
        paths_0 = _find_paths(A, elem[0])
        paths_1 = _find_paths(A, elem[1])    
        cycles.append(_find_cicle(paths_0, paths_1))
    cycles = [cycle for cycle in cycles if cycle != []]
    
    new_archs = []
    for cycle in cycles:
        new_archs.extend(_break_cycle(cycle))
    
    new_archs = set(new_archs)
    print(new_archs)
       
    return Graph(graph.get_nodes(), out)

def _break_cycle(cycle: List) -> List:
    new_archs = []
    master_node = cycle[0]
    cycle = cycle[2:-2]

    for node in cycle:
        new_archs.append((master_node, node))


    return new_archs

def _find_cicle(paths_0: List, paths_1: List) -> List:
    cycle = []
    for path_0 in paths_0:
        for node_0 in path_0[1:-1]:
            for path_1 in paths_1:
                for node_1 in path_1[1:-1]:
                    if node_0 == node_1:
                        cycle.extend(path_1[:path_1.index(node_1)+1])
                        cycle.reverse()
                        cycle.extend(path_0[:path_0.index(node_0)+1])
                        return cycle
                    
    return []

def _find_paths(adj_matrix: np.ndarray, start_node_index: int) -> List:
    paths_0 = [[start_node_index]] #lista in cui al termine avrò tutti i cammini
    n = adj_matrix.shape[0]
    
    #Risalgo su tutti i possibili cammini finchè tutti non sono terminati (i nodi non hanno genitori)
    while not all(v[-1] == '$' for v in paths_0):
        new_paths_0 = [] #lista in cui salverò i cammini estesi con i parent dell'ultimo nodo
        remove_paths_0 = [] # lista in cui salverò tutti i cammini che verranno estesi poichè sono da rimuovere
        for path in paths_0: #Per ogni cammino trovato finora....
            if path[-1] != '$': #Controllo che il cammino non sia già terminato
                base_path = path[:] #Salvo il cammino fino al punto in cui sono arrivato
                path.append('$') #Termino il cammino, se non lo estenderò avrò terminato questo cammino altrimenti la sentinella verrà tolta poi
                parents = [row for row in range(n) if adj_matrix[row, path[-2]] == 1] #cerco tutti i parent dell'ultimo nodo del cammino
                if parents != []: #Se l'ultimo nodo ha almeno un parent...
                    remove_paths_0.append(path) #Estenderò il cammino quindi lo dovrò togliere dalla lista dei cammini finale per non avere un prefisso(inutile) di un cammino completo
                    for parent in parents: #Per ogni parent dell'ultimo nodo...
                        base_path.append(parent) #Aggiungo il parent al cammino a cui ero arrivato finora
                        new_paths_0.append(base_path) #Salvo il nuovo cammino nella lista temporanea dei cammini
                        base_path = base_path[:-1] #Rimuovo l'ultimo parent inserito, se ho altri parent avrò una biforcazione del cammino
        paths_0 = [x for x in paths_0 if not x in remove_paths_0] #Rimuovo i prefissi dei cammini che ho esteso lasciando solo quelli che sono già terminati
        paths_0.extend(new_paths_0) #Aggiungo i cammini che ho esteso a quelli terminati 
    return paths_0


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
