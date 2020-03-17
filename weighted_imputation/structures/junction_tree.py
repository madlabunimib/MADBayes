from __future__ import annotations

from typing import TYPE_CHECKING

import matplotlib.pyplot as plt
import networkx as nx

from .tree import Node, Tree

if TYPE_CHECKING:
    from typing import Dict, List, Tuple
    from .graph import DirectedGraph, Graph


def _build_junction_tree(graph: DirectedGraph, chain: List) -> Node:
    chain = [tuple(clique) for clique in chain]
    nodes = {clique: _node_from_clique(graph, clique) for clique in chain}
    # Build Junction Tree from the chain
    n = len(chain)
    # For each clique in the chain
    root = nodes[chain[0]]
    for i in range(1, n):
        Ci = chain[i]
        Ck = _max_common_clique(chain[:i], Ci)
        _add_separator(graph, nodes[Ck], nodes[Ci])
    return root

def _node_from_clique(graph: DirectedGraph, clique: List) -> Node:
    items = list(clique)
    node = Node(str(items))
    node['type'] = 'clique'
    node['nodes'] = items
    node['clique'] = graph.subgraph(items)
    return node

def _max_common_clique(chain: List, Ci: Tuple) -> List:
    maxs = [set(Ci).intersection(set(clique)) for clique in chain]
    maxs = [len(common) for common in maxs]
    return chain[maxs.index(max(maxs))]

def _add_separator(graph: DirectedGraph, parent: Node, child: Node) -> None:
    separator_nodes = list(set(parent['nodes']).intersection(set(child['nodes'])))
    separator_label = parent.get_label() + '_' + str(separator_nodes) + '_' + child.get_label()
    separator = Node(separator_label)
    separator.set_parent(parent)
    child.set_parent(separator)
    separator['type'] = 'separator'
    separator['nodes'] = separator_nodes
    separator['clique'] = graph.subgraph(separator_nodes)


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
    
    @classmethod
    def from_graph_and_chain(cls, graph: Graph, chain: List) -> None:
        root = _build_junction_tree(graph, chain)
        return cls(root)
