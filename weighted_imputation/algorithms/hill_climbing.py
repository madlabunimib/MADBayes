from copy import deepcopy
from itertools import product

from ..structures import DirectedGraph, Dataset
from . import bds_score

import weighted_imputation as wi


def hill_climbing(dataset: Dataset):

    nodes = list(dataset.data.columns)
    best_dag = DirectedGraph(nodes=nodes)
    best_dag_score = bds_score(best_dag, dataset)

    all_edges = list(product(nodes, nodes))
    
    progress = True
    while progress:
        progress = False
        
        dag = DirectedGraph(nodes, best_dag.adjacency_matrix())
        dag_edges = dag.get_edges()
        reversed_dag_edges = [(edge[1], edge[0]) for edge in dag_edges]

        print(dag_edges)
        
        add_edges = [edge for edge in all_edges if edge not in dag_edges and edge not in reversed_dag_edges]
        # TRY ADDING EDGES NOT IN DAG
        for edge in add_edges:
            if edge[0] != edge[1]:
                dag.add_edge(edge[0], edge[1])
                dag_score = bds_score(dag, dataset)
                # if adding that edge does not create a loop
                if dag_score > best_dag_score:
                    best_dag.add_edge(edge[0], edge[1])
                    best_dag_score = dag_score
                    progress = True
                    
                dag.remove_edge(edge[0], edge[1])


        # TRY REMOVING DAG'S EDGES
        for edge in dag_edges:
            dag.remove_edge(edge[0], edge[1])
            dag_score = bds_score(dag, dataset)

            if dag_score > best_dag_score:
                best_dag.remove_edge(edge[0], edge[1])
                best_dag_score = dag_score
                progress = True

            dag.add_edge(edge[0], edge[1])


        # TRY REVERSE DAG'S EDGES
        for edge in dag_edges:
            dag.remove_edge(edge[0], edge[1])
            dag.add_edge(edge[1], edge[0])
            dag_score = bds_score(dag, dataset)
            # if adding that edge does not create a loop
            if dag_score > best_dag_score:
                best_dag.remove_edge(edge[0], edge[1])
                best_dag.add_edge(edge[1], edge[0])
                best_dag_score = dag_score
                progress = True

            dag.add_edge(edge[0], edge[1])
            dag.remove_edge(edge[1], edge[0])


    best_dag.plot()   
    return