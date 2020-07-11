import numpy as np
from . import madbayes as mb


def test_graph():
    # Test base constructor
    graph = mb.backend.Graph()

    # Test costructor by nodes
    nodes = ['A', 'B', 'C']
    graph = mb.backend.Graph(nodes=nodes)
    assert(graph.nodes == nodes)

    # Test constructor by adjacency_matrix
    N = 5
    p = 0.7
    adjacency_matrix = np.random.choice(
        a=[False, True], size=(N, N), p=[p, 1-p])
    graph = mb.Graph(adjacency_matrix=adjacency_matrix)


def test_graph_nodes():
    # Test node getter
    nodes = ['A', 'B', 'C']
    graph = mb.backend.Graph(nodes=nodes)
    assert(graph.nodes == nodes)

    # Test node setter
    nodes = ['E', 'D', 'F']
    graph.nodes = nodes
    assert(graph.nodes == nodes)

    # Test adding a node
    graph.add_node('A')
    assert(graph.nodes == nodes + ['A'])

    # Test removing a node
    graph.remove_node('D')
    assert(graph.nodes == ['E', 'F', 'A'])

def test_graph_edges():
    # Test edge getter
    edges = [('A', 'B'), ('B', 'C')]
    graph = mb.backend.Graph(edges=edges)
    assert(graph.edges == edges)

    # Test adding an edge
    graph.add_edge('A', 'C')
    assert(graph.edges == edges + [('A', 'C')])

    # Test removing an edge
    graph.remove_edge('B', 'C')
    assert(graph.edges == [('A', 'B'), ('A', 'C')])
