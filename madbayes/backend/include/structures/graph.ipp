#pragma once

#include "graph.hpp"

namespace madbayes {

namespace structures {

Graph::Graph(const igraph_t *other) {
    igraph_copy(&graph, other);
}

Graph::Graph(const Nodes &_n, bool mode) {
    igraph_empty(&graph, _n.size(), mode);
    set_nodes(_n);
}

Graph::Graph(const Graph &other) : nodes(other.nodes) {
    igraph_copy(&graph, &other.graph);
}

Graph &Graph::operator=(const Graph &other) {
    if (this != &other) {
        Graph tmp(other);
        std::swap(tmp.graph, graph);
        std::swap(tmp.nodes, nodes);
    }
    return *this;
}

Graph::~Graph() {
    igraph_destroy(&graph);
}

Nodes Graph::get_nodes() const {
    Nodes keys;
    for(auto it = nodes.begin(); it != nodes.end(); ++it) {
        keys.push_back(it->first);
    }
    return keys;
}

void Graph::set_nodes(const Nodes &_n) {
    if (_n.size() != size()) throw std::runtime_error("Labels must have size equals to nodes."); 
    for (size_t i = 0; i < _n.size(); i++) nodes[_n[i]] = i;
}

size_t Graph::size() const {
    return igraph_vcount(&graph);
}

bool Graph::is_directed() const {
    return igraph_is_directed(&graph);
}

bool Graph::is_chordal() const {
    igraph_bool_t result;
    igraph_is_chordal(&graph, 0, 0, &result, 0, 0);
    return result;
}

}  // namespace structures

}  // namespace madbayes