from ..structures import DirectedGraph, Node, JunctionTree
from typing import List, Set, Dict, Tuple


def build_junction_tree(graph: DirectedGraph, cliques: List) -> JunctionTree:
    nodes = graph.get_nodes()
    
    tree_nodes = _tree_nodes_from_cliques(graph, cliques)
    nodes_cliques = _build_nodes_clique_dictionary(nodes, tree_nodes)
    clique_neighborhood = _build_clique_neighborhood(nodes_cliques, tree_nodes)
    clique_neighborhood_cardinality = _clique_neighborhood_cardinality(clique_neighborhood)
    
    queue = [_max_neighborhood_cardinality(clique_neighborhood_cardinality)]

    junction_tree = JunctionTree(queue[0], nodes_cliques)

    while queue != []:
        parent = queue.pop(0)
        for neighbor in clique_neighborhood[parent]:
            separator = _build_separator(graph, parent, neighbor)
            separator.set_parent(parent)
            neighbor.set_parent(separator)
            queue.append(neighbor)
        for leaf in queue:
            for clique in clique_neighborhood:
                try:
                    clique_neighborhood[clique].remove(leaf)
                except KeyError:
                    pass

    return junction_tree

def _tree_nodes_from_cliques(graph: DirectedGraph, cliques: List) -> List[Node]:
    tree_nodes = []
    for clique in cliques:
        tree_node = Node(str(clique))
        tree_node['type'] = 'clique'
        tree_node['nodes'] = clique
        tree_node['clique'] = graph.subgraph(clique)
        tree_nodes.append(tree_node)
    return tree_nodes

def _build_nodes_clique_dictionary(nodes: List, tree_nodes: List[Node]) -> Dict:    
    nodes_cliques = {node: [] for node in nodes}
    for node in nodes:
        for tree_node in tree_nodes:
            if node in tree_node['nodes']:
                nodes_cliques[node].append(tree_node)
    return nodes_cliques

def _build_clique_neighborhood(nodes_cliques: Dict, tree_nodes: List[Node]) -> Dict:
    clique_neighborhood = {clique: set() for clique in tree_nodes}
    for node in tree_nodes:
        for node_in_clique in node["nodes"]:
            for neighbor_clique in nodes_cliques[node_in_clique]:
                if neighbor_clique != node:
                    clique_neighborhood[node].add(neighbor_clique)
    return clique_neighborhood

def _clique_neighborhood_cardinality(clique_neighborhood: Dict) -> Dict:
    return {key : len(clique_neighborhood[key]) for key in clique_neighborhood.keys()}

def _max_neighborhood_cardinality(clique_neighborhood_cardinality: Dict) -> Tuple:
    return max(clique_neighborhood_cardinality, key=clique_neighborhood_cardinality.get)

def _build_separator(graph: DirectedGraph, parent: Node, child: Node) -> Node:
    raise NotImplementedError
    return Node('')
