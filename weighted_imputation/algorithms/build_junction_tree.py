from ..structures import Graph
from typing import List, Set, Dict


def build_junction_tree(graph: Graph, cliques: List):

    #cliques = [{a,b,c}, {b,c},....]

    



    return

def build_nodes_clique_dictionary(nodes: Set, cliques: List) -> Dict:

    nodes_clique_dict = {key: [] for key in nodes}

    for clique in cliques:
        for node in clique:
            nodes_clique_dict[node].append(clique)

    return nodes_clique_dict

def build_clique_neighborhood(nodes_clique_dict: Dict, cliques: List) -> List[Set]:

    return
