#pragma once

#include "directed_graph.hpp"

namespace madbayes {

namespace structures {

DirectedGraph::DirectedGraph(const igraph_t *other) {
    int status = igraph_copy(&graph, other);
    handle_status(status);
}

DirectedGraph::DirectedGraph(int64_t nodes) : Graph(nodes, IGRAPH_DIRECTED) {}

DirectedGraph::DirectedGraph(const DirectedGraph &other) : Graph() {
    int status = igraph_copy(&graph, &other.graph);
    handle_status(status);
}

DirectedGraph &DirectedGraph::operator=(const DirectedGraph &other) {
    if (this != &other) {
        DirectedGraph tmp(other);
        std::swap(tmp.graph, graph);
    }
    return *this;
}

DirectedGraph::~DirectedGraph() {
    int status = igraph_destroy(&graph);
    handle_status(status);
}

bool DirectedGraph::is_dag() const {
    igraph_bool_t result;
    int status = igraph_is_dag(&graph, &result);
    handle_status(status);
    return result;
}

Graph DirectedGraph::to_undirected() {
    int status = 0;
    igraph_t undirected;
    status = igraph_copy(&undirected, &graph);
    handle_status(status);
    status = igraph_to_undirected(&undirected, IGRAPH_TO_UNDIRECTED_COLLAPSE, 0);
    handle_status(status);
    Graph result(&undirected);
    status = igraph_destroy(&undirected);
    handle_status(status);
    return result;
}

}  // namespace structures

}  // namespace madbayes