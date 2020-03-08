import networkx as nx
import matplotlib.pyplot as plt
from typing import Dict
from .graph import DirectedGraph
from .tree import Node, Tree


class JunctionTree(Tree):
    
    def __init__(self, root: Node, nodes_in_cliques: Dict = None) -> None:
        super().__init__(root)
        if nodes_in_cliques is None:
            self._nodes = {}
            self._index(self._root)
        else:
            self._nodes = nodes_in_cliques
    
    def _index(self, node: Node) -> None:
        # For each node of a clique
        for item in node['clique'].get_nodes():
            # If the node is not in the index
            # then add an empty list in the index
            if item not in self._nodes.keys():
                self._nodes[item] = []
            # Append the node in which the clique
            # is located to the corresponding list
            self._nodes[item].append(node)
        # Repeat for each child of the node
        for child in node.get_children():
            self._index(child)
    
    def plot(self) -> None:
        G = self.to_directed_graph().to_networkx()
        layout = nx.nx_pydot.graphviz_layout(G, prog='dot')
        types = nx.get_node_attributes(G, 'type')
        shapes = {
            'clique': 'o',      # Circle
            'separator': 's'    # Square
        }
        for node in G.nodes:
            shape = shapes[nx.get_node_attributes(G, 'type')[node]]
            nx.draw_networkx_nodes(G, layout, nodelist=[node], node_shape=shape, node_color='red')
            nx.draw_networkx_edges(G, layout)
        nx.draw_networkx_labels(G, layout)
        plt.show()
