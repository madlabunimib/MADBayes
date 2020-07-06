#pragma once

#include "graph.hpp"

namespace madbayes {

namespace structures {

Graph::Graph(int64_t nodes) {
    size_t flag = igraph_empty(&graph, nodes, IGRAPH_UNDIRECTED);
    if (flag == IGRAPH_EINVAL) throw std::runtime_error("Invalid number of vertices");
}

Graph::Graph(const Graph &other) {
    igraph_copy(&graph, &other.graph);
}

Graph &Graph::operator=(const Graph &other) {
    if (this != &other) {
        Graph tmp(other);
        std::swap(tmp.graph, graph);
    }
    return *this;
}

Graph::~Graph() {
    igraph_destroy(&graph);
}

size_t Graph::size() const {
    return igraph_vcount(&graph);
}

}  // namespace structures

}  // namespace madbayes