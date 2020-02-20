import networkx as nx
from ..structure import Graph, Prefix_tree


def to_networkx(graph: Graph) -> nx.Graph:
    mapping = {
        k:v
        for k,v in enumerate(graph.get_nodes())
    }
    G = nx.DiGraph(graph.get_adjacency_matrix())
    G = nx.relabel_nodes(G, mapping)
    return G

def prefix_tree_to_networkx(graph: Prefix_tree) -> nx.Graph:
    mapping = {
        k:v
        for k,v in enumerate(graph.get_nodes())
    }
    G = nx.DiGraph(graph.get_adjacency_matrix())
    G = nx.relabel_nodes(G, mapping)
    return G

def from_networkx(G: nx.Graph) -> Graph:
    nodes = [str(node) for node in G.nodes]
    adjacent_matrix = nx.to_numpy_array(G).astype(bool)
    return Graph(nodes, adjacent_matrix)
