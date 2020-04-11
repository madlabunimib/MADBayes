from __future__ import annotations

from copy import deepcopy
from functools import reduce
from typing import TYPE_CHECKING

import matplotlib.pyplot as plt
import networkx as nx

from .tree import Node, Tree

if TYPE_CHECKING:
    from typing import Dict, List, Tuple
    from .graph import DirectedGraph, Graph
    from .probability_table import ProbabilityTable


class JunctionTree(Tree):
    
    def __init__(self, root: Node) -> None:
        self._nodes = {}
        self._cliques = []
        super().__init__(root)
        self._calibrate()
    
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
    
    def query(self, method: str, variables: List, evidences: Dict = None) -> List:
        jt = self
        if evidences is not None:
            jt = self.set_evidences(**evidences)
        results = [
            jt[variable][0]['belief'].marginalize({variable})
            for variable in variables
        ]
        if method == 'joint' or method == 'conditional':
            joint = reduce(lambda a, b: a * b, results, 1)
            if method == 'joint':
                return [joint]
            if method == 'conditional':
                condition = reduce(lambda a, b: a * b, results[1:], 1)
                return [joint/condition]
        return results
    
    def set_evidences(self, **kwargs) -> 'JunctionTree':
        jt = deepcopy(self)
        for variable, value in kwargs.items():
            jt._absorb_evidence(variable, value)
        return jt
    
    def _absorb_evidence(self, variable: str, value: str) -> None:
        # Select the first clique that constains variable
        clique = self[variable][0]
        old_margin = clique['belief'].marginalize([variable])
        new_margin = old_margin.copy()
        new_margin.loc[:] = 0
        new_margin.loc[value] = 1
        clique['belief'] = clique['belief'] / old_margin * new_margin
        self._calibrate_downward(None, clique, 1)
    
    def _calibrate(self) -> None:
        root = self.root()
        # Upward phase
        root['belief'] = self._calibrate_upward(None, root)
        # Downward phase
        self._calibrate_downward(None, root, 1)

    def _calibrate_upward(self, source: Node, target: Node) -> ProbabilityTable:
        if target['type'] == 'separator':
            # Pass the message down in the tree
            clique = target.neighbors().difference({source})[0]
            message = self._calibrate_upward(target, clique)
            # Save the returning message
            target['belief'] = message
        if target['type'] == 'clique':
            # Gather the messages
            message =  [
                self._calibrate_upward(target, node)
                for node in target.neighbors().difference({source})
            ]
            # Compute the clique belief
            message = reduce(lambda a, b: a * b, message, 1)
            target['belief'] = target['potential'] * message
            # Compute the message
            marginal = target['nodes']
            if source is not None:
                marginal = source['nodes']
            message = target['belief'].marginalize(marginal)
        return message
    
    def _calibrate_downward(self, source: Node, target: Node, message: ProbabilityTable) -> None:
        if target['type'] == 'separator':
            # Compute message using belief
            message = message.marginalize(target['nodes']) / target['belief']
            # Compute sepset belief
            target['belief'] = target['belief'] * message
            # Pass the message down in the tree
            clique = target.neighbors().difference({source})[0]
            self._calibrate_downward(target, clique, message)
        if target['type'] == 'clique':
            # Compute the final belief
            target['belief'] = target['belief'] * message
            # Propagate the belief
            for node in target.neighbors().difference({source}):
                self._calibrate_downward(target, node, target['belief'])
    
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
