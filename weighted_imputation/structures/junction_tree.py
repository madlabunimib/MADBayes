import networkx as nx
import matplotlib.pyplot as plt
import xarray as xa
import numpy as np
import itertools
from typing import Dict, List, Tuple
from queue import Queue
from .graph import Graph, DirectedGraph
from .tree import Node, Tree
from ..algorithms.moralize import moralize
from ..algorithms.triangulate import triangulate
from ..algorithms.chain_of_cliques import chain_of_cliques
from ..utils import get_cpts
from copy import deepcopy, copy

import pprint as pp


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
    def from_graph(cls, graph: Graph) -> None:
        moralized = graph
        if graph.is_directed():
            moralized = moralize(graph)            
        triangulated = triangulate(moralized)
        chain = chain_of_cliques(triangulated)
        root = _build_junction_tree(graph, chain)
        return cls(root)

"""
def compute_potentials(jt: JunctionTree, cpts_file: Dict):

    cpts_dict = get_cpts(cpts_file)
    margin_table_cache = build_margin_table_cache(cpts_file, cpts_dict)

    queue = Queue()
    queue.put(jt.get_root())
    while not queue.empty():
        node = queue.get()
        for child in node.get_children():
            queue.put(child)
        
        if node["type"] == "clique":
            node["potential"] = compute_clique_potential(node, cpts_dict, margin_table_cache)
        else:
            node["potential"] = compute_separator(node, node.get_parent(), cpts_dict)

def compute_clique_potential(clique: Node, cpts_dict: Dict, margin_table_cache: Dict):

    #Compute dimensions
    dimensions = clique["nodes"]
    #Compute coordinates
    coordinates = [cpts_dict[node].coords[node].values for node in clique["nodes"]]
    #Compute size of n-d-matrix
    levels = [len(cpts_dict[dim].coords[dim].values) for dim in dimensions]

    potential = xa.DataArray(np.ones(shape=levels), dims=dimensions, coords=coordinates)

    nodes_in_clique = copy(clique["nodes"])
    while nodes_in_clique != []:
        node = nodes_in_clique.pop()
        parents = clique["clique"].parents(node)
        
        node_dict_key = key_dict(node, parents)
        if node_dict_key not in margin_table_cache:
            margin_table = compute_margin_table(node, parents, cpts_dict, margin_table_cache)
        else:
            margin_table = margin_table_cache[node_dict_key]

        dims_order = list(margin_table.dims)
        margin_values = []
        for dim in dims_order:
            margin_values.append([value for value in margin_table[dim].coords[dim].values])

        dims_order.extend([x for x in clique["nodes"] if x not in dims_order])
        potential = potential.transpose(*dims_order)
        for combination in list(itertools.product(*margin_values)):
            potential.loc[tuple(combination)] = potential.loc[tuple(combination)] * \
                margin_table.loc[tuple(combination)]
    
    return potential
"""

def compute_margin_table(node: str, parents: List[str], cpts_dict: Dict, margin_table_cache: Dict) -> Dict:
    
    node_cpt = deepcopy(cpts_dict[node])

    # Levels of dependant
    node_values = [key for key in node_cpt.coords[node].values]
    # Dependencies
    node_dependencies = [x for x in node_cpt.coords if x != node]
    # Levels of dependencies
    dependencies_values = {
        dependencie : [value for value in cpts_dict[dependencie].coords[dependencie].values]
        for dependencie in node_dependencies
        }

    # If dependencies not empy
    if not dependencies_values == {}:
        # For each level of dependant
        for node_value in node_values:
            # For each combination of dependencies levels
            for combination in list(_my_product(dependencies_values)):
                # Partial dimensional access vector
                label = [x for x in combination.values()]
                # Complete dimensioal access vector
                label.insert(0, node_value)
                # For node in dependencies
                for item in combination:
                    # If not cache compute margin table
                    if not item in margin_table_cache:
                        # Recursive call
                        compute_margin_table(item, [], cpts_dict, margin_table_cache)
                    # JPT'[A] = JPT'[A] * TODO
                    node_cpt.loc[tuple(label)] = node_cpt.loc[tuple(label)] * \
                        margin_table_cache[item].loc[combination[item]]

        # MARGINALIZE
        #Compute dimensions of the margin table (node + parents)
        dims_order = [node]
        dims_order.extend(parents)

        # Init Margine Table
        #Compute coordinates of the margin table 
        coordinates = [node_values]
        if parents != []:
            coordinates.extend([dependencies_values[x] for x in dependencies_values if x in parents])
        #Compute size of the margin table
        levels = [len(coord) for coord in coordinates]

        margin_table = xa.DataArray(np.zeros(shape=levels), dims=dims_order, coords=coordinates)
        
        # Reorder JPD using new dimension order
        dims_order.extend([x for x in node_cpt.coords if x not in dims_order])
        node_cpt = node_cpt.transpose(*dims_order)

        # MT dimensions
        node_and_parents = [node]
        node_and_parents.extend(parents)
        
        parents_values_dict = {
            parent : [value for value in cpts_dict[parent].coords[parent].values]
            for parent in node_and_parents
            }
        for combination in _my_product(parents_values_dict):
            label = [x for x in combination.values()]
            # Marginalize
            margin_table.loc[tuple(label)] = node_cpt.loc[tuple(label)].sum()
    
    else:
        margin_table = node_cpt
    
    margin_table_cache.update({key_dict(node, parents) : margin_table}) 
    return margin_table

def compute_separator(node: Node, parent: Node, cpts_dict: Dict) -> Dict:

    parent_cpt = deepcopy(parent["potential"])
    
    #Compute dimensions of the margin table
    dimensions = node["nodes"]
    #Compute coordinates of the margin table 
    coordinates = [cpts_dict[dim].coords[dim].values for dim in dimensions]
    #Compute size of the margin table
    levels = [len(coord) for coord in coordinates]

    margin_table = xa.DataArray(np.zeros(shape=levels), dims=dimensions, coords=coordinates)

    dimensions.extend([dim for dim in parent["nodes"] if dim not in dimensions])
    parent_cpt = parent_cpt.transpose(*dimensions)

    for combination in itertools.product(*coordinates):
        margin_table.loc[tuple(combination)] = parent_cpt.loc[tuple(combination)].sum()

    return margin_table

"""
def build_margin_table_cache(cpts_file: Dict, cpts_dict: Dict) -> Dict:
    margin_table_cache = {}
    for node in cpts_dict:
        parents = cpts_file[node]["dependencies"]
        margin_table_cache.update({key_dict(node, parents) : cpts_dict[node]})
    return margin_table_cache

def _my_product(input: Dict):
    return (dict(zip(input.keys(), values)) for values in itertools.product(*input.values()))

def key_dict(node: str, parents: List[str]) -> str:
    node_dict_key = node + "|"
    for parent in parents:
        node_dict_key += parent + ":"
    return node_dict_key[:-1]
"""
 