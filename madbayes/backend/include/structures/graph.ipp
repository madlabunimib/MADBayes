#pragma once

#include "graph.hpp"

namespace madbayes {

namespace structures {

Graph::Graph(const igraph_t *other) {
    igraph_copy(&graph, other);
}

Graph::Graph(const Labels &_n, bool mode) {
    igraph_empty(&graph, _n.size(), mode);
    set_labels(_n);
}

Graph::Graph(const Graph &other) : labels(other.labels) {
    igraph_copy(&graph, &other.graph);
}

Graph &Graph::operator=(const Graph &other) {
    if (this != &other) {
        Graph tmp(other);
        std::swap(tmp.graph, graph);
        std::swap(tmp.labels, labels);
    }
    return *this;
}

Graph::~Graph() {
    igraph_destroy(&graph);
}

Labels Graph::get_labels() const {
    Labels keys;
    for(auto it = labels.begin(); it != labels.end(); ++it) {
        keys.push_back(it->first);
    }
    return keys;
}

void Graph::set_labels(const Labels &_n) {
    if (_n.size() != size()) throw std::runtime_error("Labels must have size equals to labels."); 
    for (size_t i = 0; i < _n.size(); i++) labels[_n[i]] = i;
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