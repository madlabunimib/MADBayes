import networkx as nx
from ..structure import Graph, PrefixTree

def prefix_tree_to_networkx(graph: PrefixTree) -> nx.Graph:
    mapping = {
        k:v
        for k,v in enumerate(graph.get_nodes())
    }
    G = nx.DiGraph(graph.get_adjacency_matrix())
    G = nx.relabel_nodes(G, mapping)
    return G
