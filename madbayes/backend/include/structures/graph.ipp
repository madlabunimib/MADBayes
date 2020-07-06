#pragma once

#include "graph.hpp"

namespace madbayes {

namespace structures {

void handle_status(int status) {
    if (status != IGRAPH_SUCCESS) {
        throw std::runtime_error(igraph_strerror(status));
    }
}

Graph::Graph() {}

Graph::Graph(const igraph_t *other) {
    int status = igraph_copy(&graph, other);
    handle_status(status);
}

Graph::Graph(int64_t nodes, bool mode) {
    int status = igraph_empty(&graph, nodes, mode);
    handle_status(status);
}

Graph::Graph(const Graph &other) {
    int status = igraph_copy(&graph, &other.graph);
    handle_status(status);
}

Graph &Graph::operator=(const Graph &other) {
    if (this != &other) {
        Graph tmp(other);
        std::swap(tmp.graph, graph);
    }
    return *this;
}

Graph::~Graph() {
    int status = igraph_destroy(&graph);
    handle_status(status);
}

size_t Graph::size() const {
    return igraph_vcount(&graph);
}

bool Graph::is_directed() const {
    return igraph_is_directed(&graph);
}

bool Graph::is_chordal() const {
    igraph_bool_t result;
    int status = igraph_is_chordal(&graph, 0, 0, &result, 0, 0);
    handle_status(status);
    return result;
}

}  // namespace structures

}  // namespace madbayes