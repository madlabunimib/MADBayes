from copy import deepcopy
from itertools import product

from ..structures import DirectedGraph, Dataset
from .breadth_first_search import is_reachable
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
        
        dag = deepcopy(best_dag)
        edges = dag.edges()
        reversed_dag_edges = [(edge[1], edge[0]) for edge in edges]
        
        add_edges = [
            edge 
            for edge in all_edges 
            if edge not in edges 
            and edge not in reversed_dag_edges
            and edge[0] != edge[1]]
        
        # TRY ADDING EDGES NOT IN DAG
        for edge in add_edges:
            dag.add_edge(*edge)
            dag_score = bds_score(dag, dataset)
            
            #Check for cycle
            if not is_reachable(graph=dag, source=edge[1], destination=edge[0]):
                if dag_score > best_dag_score:
                    best_dag = deepcopy(dag)
                    best_dag_score = dag_score
                    progress = True
                    
                    
            dag.remove_edge(*edge)



        dag = deepcopy(best_dag)
        # TRY REMOVING DAG'S EDGES
        for edge in edges:
            dag.remove_edge(*edge)
            dag_score = bds_score(dag, dataset)

            if dag_score > best_dag_score:
                best_dag = deepcopy(dag)
                best_dag_score = dag_score
                progress = True

            dag.add_edge(*edge)



        dag = deepcopy(best_dag)
        # TRY REVERSE DAG'S EDGES
        for edge in edges:
            dag.reverse_edge(*edge)
            dag_score = bds_score(dag, dataset)
            #Check for cycle
            if not is_reachable(graph=dag, source=edge[0], destination=edge[1]):
                if dag_score > best_dag_score:
                    best_dag = deepcopy(dag)
                    best_dag_score = dag_score
                    progress = True

            dag.reverse_edge(edge[1], edge[0])


        best_dag.plot()   
    return
