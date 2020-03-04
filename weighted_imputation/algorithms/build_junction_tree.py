from ..structures import Graph
from typing import List, Set, Dict
import matplotlib.pyplot as plt
import networkx as nx


def build_junction_tree(graph: Graph, cliques: List) -> nx.Graph:

    #cliques = [{a,b,c}, {b,c},....]
    nodes = graph.get_nodes()

    nodes_clique_dict = _build_nodes_clique_dictionary(nodes, cliques)
    clique_neighborhood = _build_clique_neighborhood(nodes_clique_dict, cliques)

    leafs = [_find_max_neighborhood_cardinality(_compute_clique_neighborhood_cardinality(clique_neighborhood))]
    ###
    junction_tree = nx.Graph()
    ###

    while leafs != []:
        node = leafs.pop(0)
        junction_tree.add_node(node)#
        for neighbor in clique_neighborhood[node]:
            junction_tree.add_node(neighbor)#
            junction_tree.add_edge(node, neighbor)#
            leafs.append(neighbor)
        for leaf in leafs:
            for clique in clique_neighborhood:
                if leaf in clique_neighborhood[clique]:
                    clique_neighborhood[clique].remove(leaf)

    return junction_tree

def _build_nodes_clique_dictionary(nodes: Set, cliques: List) -> Dict:
    nodes_clique_dict = {key: [] for key in nodes}
    for clique in cliques:
        for node in clique:
            nodes_clique_dict[node].append(clique)

    return nodes_clique_dict

def _build_clique_neighborhood(nodes_clique_dict: Dict, cliques: List) -> Dict:
    clique_neighborhood = {tuple(key): set() for key in cliques}
    for clique in cliques:
        for node in clique:
            for neighbor_clique in nodes_clique_dict[node]:
                if neighbor_clique != clique:
                    clique_neighborhood[tuple(clique)].add(tuple(neighbor_clique))

    return clique_neighborhood

def _compute_clique_neighborhood_cardinality(clique_neighborhood: Dict) -> Dict:
    return {key : len(clique_neighborhood[key]) for key in clique_neighborhood.keys()}

def _find_max_neighborhood_cardinality(clique_neighborhood_cardinality: Dict) -> Dict:
    return max(clique_neighborhood_cardinality, key=clique_neighborhood_cardinality.get)
