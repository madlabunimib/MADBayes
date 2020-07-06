#pragma once

#include "directed_graph.hpp"

namespace madbayes {

namespace structures {

DirectedGraph::DirectedGraph(const igraph_t *other) : Graph(other) {}

DirectedGraph::DirectedGraph(const Nodes &labels) : Graph(labels, IGRAPH_DIRECTED) {}

DirectedGraph::DirectedGraph(const Graph &other) : Graph(other) {
    igraph_to_directed(&graph, IGRAPH_TO_DIRECTED_MUTUAL);
}

DirectedGraph::DirectedGraph(const DirectedGraph &other) : Graph(other) {}

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
    igraph_bool_t out;
    igraph_is_dag(&graph, &out);
    return out;
}

Graph DirectedGraph::to_undirected() {
    igraph_t undirected;
    igraph_copy(&undirected, &graph);
    igraph_to_undirected(&undirected, IGRAPH_TO_UNDIRECTED_COLLAPSE, 0);
    Graph out(&undirected);
    igraph_destroy(&undirected);
    return out;
}

}  // namespace structures

}  // namespace madbayes