import matplotlib.pyplot as plt 
import networkx as nx 
from ..utils import transform
from ..structure import Graph


def plot_graph(g: Graph) -> None:
    g = transform.to_networkx(g)
    nx.draw(g, with_labels = True)
    plt.show()

def plot_networkx_graph(g: nx.Graph) -> None:
    nx.draw(g, with_labels = True)
    plt.show()
