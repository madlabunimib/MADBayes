from ..structures import DirectedGraph, Node, JunctionTree
from typing import List, Set, Dict, Tuple


def build_junction_tree(graph: DirectedGraph, cliques: List) -> JunctionTree:
    nodes = graph.get_nodes()
    
    tree_nodes = _tree_nodes_from_cliques(graph, cliques)
    nodes_cliques = _build_nodes_clique_dictionary(nodes, tree_nodes)
    clique_neighborhood = _build_clique_neighborhood(nodes_cliques, tree_nodes)    
    root = _select_junction_tree_root(clique_neighborhood)
    junction_tree = JunctionTree(root, nodes_cliques)

    queue = [root]
    while queue != []:
        parent = queue.pop(0)
        for neighbor in clique_neighborhood[parent]:
            _add_separator(graph, parent, neighbor)
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
        for node_in_clique in node['nodes']:
            for neighbor_clique in nodes_cliques[node_in_clique]:
                if neighbor_clique != node:
                    clique_neighborhood[node].add(neighbor_clique)
    return clique_neighborhood

def _neighborhood_cardinality(clique_neighborhood: Dict) -> Dict:
    return {key : len(clique_neighborhood[key]) for key in clique_neighborhood.keys()}

def _max_neighborhood_cardinality(clique_neighborhood_cardinality: Dict) -> Tuple:
    return max(clique_neighborhood_cardinality, key=clique_neighborhood_cardinality.get)

def _select_junction_tree_root(clique_neighborhood: Dict) -> Node:
    neighborhood_cardinality = _neighborhood_cardinality(clique_neighborhood)
    root = _max_neighborhood_cardinality(neighborhood_cardinality)
    for cliques in clique_neighborhood.values():
        try:
            cliques.remove(root)
        except KeyError:
            pass
    return root

def _add_separator(graph: DirectedGraph, parent: Node, child: Node) -> Node:
    separator_nodes = list(set(parent['nodes']).intersection(set(child['nodes'])))
    separator = Node(str(separator_nodes))
    separator.set_parent(parent)
    child.set_parent(separator)
    separator['type'] = 'separator'
    separator['nodes'] = separator_nodes
    separator['clique'] = graph.subgraph(separator_nodes)
