#pragma once

#include "directed_graph.hpp"

namespace madbayes {

namespace structures {

DirectedGraph::DirectedGraph(int64_t nodes) : Graph(nodes, IGRAPH_DIRECTED) {}

DirectedGraph::DirectedGraph(const DirectedGraph &other) : Graph() {
    igraph_copy(&graph, &other.graph);
}

DirectedGraph &DirectedGraph::operator=(const DirectedGraph &other) {
    if (this != &other) {
        DirectedGraph tmp(other);
        std::swap(tmp.graph, graph);
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

}  // namespace structures

}  // namespace madbayes