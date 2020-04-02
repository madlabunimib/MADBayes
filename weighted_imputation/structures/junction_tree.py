from __future__ import annotations

from functools import reduce
from typing import TYPE_CHECKING

import matplotlib.pyplot as plt
import networkx as nx

from .tree import Node, Tree

if TYPE_CHECKING:
    from typing import Dict, List, Tuple
    from .graph import DirectedGraph, Graph


class JunctionTree(Tree):
    
    def __init__(self, root: Node) -> None:
        self._nodes = {}
        self._cliques = []
        super().__init__(root)
    
    def _index(self, node: Node) -> None:
        if node['type'] == 'clique':
            self._cliques.append(node)
            # For each node of a clique
            for item in node['nodes']:
                # If the node is not in the index
                # then add an empty list in the index
                if item not in self._nodes.keys():
                    self._nodes[item] = []
                # Append the node in which the clique
                # is located to the corresponding list
                self._nodes[item].append(node)
        # Repeat for each child of the node
        for child in node.children():
            self._index(child)
    
    def cliques(self) -> List[Node]:
        return self._cliques.copy()
    
    def _calibration(self):
        # Upward phase
        root = self.root()
        root['beliefs'] = self._calibration_upward(root)
        # Downward phase


    def _calibration_upward(self, root: Node):
        if root['type'] == 'separator':
            clique = root.children()[0]
            messages = self._calibration_upward(clique)
            root['messages'] = messages
        if root['type'] == 'clique':
            messages =  [
                self._calibration_upward(node)
                for node in root.children()
            ]
            messages = reduce(lambda a, b: a * b, messages, 1)
            messages = root['potentials'] * messages
            marginal = root['nodes']
            if root.parent() is not None:
                marginal = marginal.intersection(root.parent()['nodes'])
            messages = messages.marginalize(marginal)
        return messages
    
    def plot(self) -> None:
        plt.figure(1, figsize=(15,15)) 
        G = self.to_directed_graph().to_networkx()
        try:
            layout = nx.nx_pydot.graphviz_layout(G, prog='dot')
        except IndexError:
            # TODO: Fix large tree
            layout = nx.spring_layout(G)
        shapes = {
            'clique': 'o',      # Circle
            'separator': 's'    # Square
        }
        for node in G.nodes:
            shape = shapes[nx.get_node_attributes(G, 'type')[node]]
            nx.draw_networkx_nodes(G, layout, nodelist=[node], node_shape=shape, node_color='red')
            nx.draw_networkx_edges(G, layout)
        lables = nx.draw_networkx_labels(G, layout)
        for _, label in lables.items():
            label.set_rotation(30)
        plt.show()
