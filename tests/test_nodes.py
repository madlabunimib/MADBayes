import numpy as np
import networkx as nx
from . import weighted_imputation as wi

def test_undirected_graph():
    nodes = [1, 10, 25, 50, 75, 100, 250]
    graphs = [
        nx.gnp_random_graph(n, 0.3, directed=False)
        for n in nodes
    ]
    neighbors = [[sorted(G.neighbors(node)) for node in G.nodes] for G in graphs]
    boundaries = [sorted(nx.algorithms.node_boundary(G, list(G.nodes)[:5])) for G in graphs]
    wi_graphs = [wi.Graph.from_networkx(G) for G in graphs]
    wi_neighbors = [[[int(n) for n in graph.neighbors(node)] for node in graph.get_nodes()] for graph in wi_graphs]
    wi_boundaries = [[int(n) for n in graph.boundary(np.array(graph.get_nodes()[:5]))] for graph in wi_graphs]
    assert(neighbors == wi_neighbors)
    assert(boundaries == wi_boundaries)

def test_directed_graph():
    # Generate random graphs from nodes count
    nodes = [1, 10, 25, 50, 75, 100, 250]
    graphs = [
        nx.gnp_random_graph(n, 0.5, directed=True)
        for n in nodes
    ]
    # Transform random graphs to DAGs by edge selection
    graphs = [
        nx.DiGraph([(u,v) for (u,v) in G.edges() if u < v])
        for G in graphs
    ]
    # Check if transformed graphs are DAGs
    are_dags = [nx.is_directed_acyclic_graph(G) for G in graphs]
    assert(all(are_dags))
    parents = [[sorted(G.predecessors(node)) for node in G.nodes] for G in graphs]
    children = [[sorted(G.successors(node)) for node in G.nodes] for G in graphs]
    ancestors = [[sorted(nx.ancestors(G, node)) for node in list(G.nodes)[:5]] for G in graphs]
    descendants = [[sorted(nx.descendants(G, node)) for node in list(G.nodes)[:5]] for G in graphs[:3]]
    wi_graphs = [wi.DirectedGraph.from_networkx(G) for G in graphs]
    wi_parents = [[sorted([int(n) for n in graph.parents(node)]) for node in graph.get_nodes()] for graph in wi_graphs]
    wi_children = [[sorted([int(n) for n in graph.children(node)]) for node in graph.get_nodes()] for graph in wi_graphs]
    wi_ancestors = [[sorted([int(n) for n in graph.ancestors(node)]) for node in graph.get_nodes()[:5]] for graph in wi_graphs]
    wi_descendants = [[sorted([int(n) for n in graph.descendants(node)]) for node in graph.get_nodes()[:5]] for graph in wi_graphs[:3]]
    assert(parents == wi_parents)
    assert(children == wi_children)
    assert(ancestors == wi_ancestors)
    assert(descendants == wi_descendants)
