import pygraphviz
import networkx as nx
import matplotlib.pyplot as plt


def plot(dot: str):
    graph = pygraphviz.AGraph(string=str(dot))
    mapper = {
        n.get_name(): n.attr['label']
        for n in graph.iternodes()
    }
    graph = nx.nx_agraph.from_agraph(graph)
    graph = nx.relabel_nodes(graph, mapper)
    nx.draw(
        graph,
        pos=nx.nx_agraph.pygraphviz_layout(graph, prog='dot'),
        with_labels=True
    )
    plt.show()
