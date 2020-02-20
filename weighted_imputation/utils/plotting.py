import matplotlib.pyplot as plt 
import networkx as nx 
from ..utils import transform
from ..structure import Graph, Prefix_tree


def plot_graph(graph: Graph) -> None:
    nx.draw(graph.to_networkx(), with_labels = True)
    plt.show()

def plot_networkx_graph(G: nx.Graph) -> None:
    nx.draw(G, with_labels = True)
    plt.show()

def plot_prefix_tree(g: Prefix_tree) -> None:
    g = transform.prefix_tree_to_networkx(g)
    nx.draw(g, with_labels = True)
    plt.show()
    