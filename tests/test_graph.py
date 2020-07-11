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
    adjacency_matrix = np.random.choice(a=[False, True], size=(N, N), p=[p, 1-p])
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
