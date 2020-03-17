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
from ..utils import get_cpts, compute_margin_table


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


def compute_potentials(jt: JunctionTree, cpts_file: Dict):

    cpts_dict = get_cpts(cpts_file)
    margin_cache = {}

    jt_root = jt.get_root()
    queue = Queue()
    queue.put(jt_root)
    while not queue.empty():
        node = queue.get()
        for child in node.get_children():
            queue.put(child)

        if node["type"] == "clique":

            nodes_in_clique = node["nodes"]
            edge_in_clique = node["clique"].get_edges()

            #Compute dimensions
            dimensions = nodes_in_clique

            #Compute coordinates
            coordinates = []
            for node in nodes_in_clique:
                coordinates.append(cpts_file[node]["levels"])
            
            #Compute size of n-d-matrix
            levels = []
            for dim in dimensions:
                levels.append(len(cpts_file[dim]["levels"]))


            data = xa.DataArray(np.ones(shape=levels), dims=dimensions, coords = coordinates)
            computed_nodes = []
            for edge in edge_in_clique:
                
                
                #Compute for dependencies variables -> parent in edge -> edge[0]
                if edge[0] not in computed_nodes:
                    if edge[0] not in margin_cache:
                        margin_table, margin_cache = compute_margin_table(edge[0], cpts_dict, margin_cache)
                    else:
                        margin_table = margin_cache[edge[0]]


                    dimensions = [edge[0]]
                    dimensions.extend([x for x in nodes_in_clique if x not in dimensions])

                    coordinates = [cpts_file[edge[0]]["levels"]]
                    for node in nodes_in_clique:
                        if node != edge[0]:
                            coordinates.append(cpts_file[node]["levels"])

                    data = data.transpose(*dimensions)
                    for combination in list(itertools.product(*coordinates)): 
                        data.loc[combination] = data.loc[combination] * \
                            margin_table.loc[combination[0]]

                    computed_nodes.append(edge[0])



                #Compute for dependant variables -> child in edge -> edge[1]
                if edge[1] not in computed_nodes:
                    dim = [x for x in dimensions if x in cpts_dict[edge[1]].coords]
                    tmp_cpt = cpts_dict[edge[1]].transpose(*dim)
                    coordinates = [cpts_file[node]["levels"] for node in dim]
                    dim.extend([x for x in dimensions if x not in dim])
                    data = data.transpose(*dim)
    
                    for combination in list(itertools.product(*coordinates)): 
                        data.loc[combination] = data.loc[combination] * \
                            tmp_cpt.loc[combination]
                    
                    computed_nodes.append(edge[1])

        else:
            pass
            #TODO COMPUTE SEPARATORS MARGIN TABLE


    return 

def compute_separator_margin_table():

    return

            