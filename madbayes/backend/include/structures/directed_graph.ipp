#pragma once

#include "directed_graph.hpp"

namespace madbayes {

namespace structures {

DirectedGraph::DirectedGraph(const igraph_t *other) : Graph(other) {}

DirectedGraph::DirectedGraph(const Nodes &nodes) : Graph(nodes, IGRAPH_DIRECTED) {}

DirectedGraph::DirectedGraph(const DirectedGraph &other) : Graph(other) {}

DirectedGraph &DirectedGraph::operator=(const DirectedGraph &other) {
    if (this != &other) {
        DirectedGraph tmp(other);
        std::swap(tmp.graph, graph);
        std::swap(tmp.nodes, nodes);
    }
    return *this;
}

DirectedGraph::~DirectedGraph() {
    igraph_destroy(&graph);
}

bool DirectedGraph::is_dag() const {
    igraph_bool_t result;
    igraph_is_dag(&graph, &result);
    return result;
}

Graph DirectedGraph::to_undirected() {
    igraph_t undirected;
    igraph_copy(&undirected, &graph);
    igraph_to_undirected(&undirected, IGRAPH_TO_UNDIRECTED_COLLAPSE, 0);
    Graph result(&undirected);
    igraph_destroy(&undirected);
    result.set_nodes(get_nodes());
    return result;
}

}  // namespace structures

}  // namespace madbayes