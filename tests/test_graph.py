import numpy as np
from . import weighted_imputation as wi

def test_graph():
    # Test base constructor
    graph = wi.Graph()

    # Test costructor by nodes
    nodes = ['A', 'B', 'C']
    graph = wi.Graph(nodes=nodes)

    # Test constructor by adjacency_matrix
    N = 5
    p = 0.7
    adjacency_matrix = np.random.choice(a=[False, True], size=(N, N), p=[p, 1-p])
    graph = wi.Graph(adjacency_matrix=adjacency_matrix)

def test_graph_nodes():
    # Test node getter
    nodes = ['A', 'B', 'C']
    graph = wi.Graph(nodes=nodes)
    assert(graph.nodes() == nodes)

    # Test node setter
    nodes = ['E', 'D', 'F']
    graph.set_nodes(nodes)
    assert(graph.nodes() == nodes)

    # Test adding a node
    graph.add_node('A')
    assert(graph.nodes() == nodes + ['A'])
