#pragma once

#include "directed_graph.hpp"

namespace madbayes {

namespace structures {

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

}  // namespace structures

}  // namespace madbayes