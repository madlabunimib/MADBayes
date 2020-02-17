import networkx as nx
from ..structure import Graph


def to_networkx(graph: Graph) -> nx.Graph:
    mapping = {
        k:v.get_label()
        for k,v in enumerate(graph.get_nodes())
    }
    G = nx.DiGraph(graph.get_adjacency_matrix())
    G = nx.relabel_nodes(G, mapping)
    return G

def from_networkx(G: nx.Graph) -> Graph:
    pass
