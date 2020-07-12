#pragma once

#include "directed_graph.hpp"

namespace madbayes {

namespace structures {

DirectedGraph::DirectedGraph() : Graph() { igraph_to_directed(&graph, IGRAPH_TO_DIRECTED_MUTUAL); }

DirectedGraph::DirectedGraph(const std::string &formula) : Graph(formula, IGRAPH_DIRECTED) {}

DirectedGraph::DirectedGraph(const Nodes &labels) : Graph(labels, IGRAPH_DIRECTED) {}

DirectedGraph::DirectedGraph(const Edges &edges) : Graph(edges, IGRAPH_DIRECTED) {}

DirectedGraph::DirectedGraph(const Graph &other) : Graph(other) {
    igraph_to_directed(&graph, IGRAPH_TO_DIRECTED_MUTUAL);
}

DirectedGraph::DirectedGraph(const DirectedGraph &other) : Graph(other) {}

DirectedGraph &DirectedGraph::operator=(const DirectedGraph &other) {
    if (this != &other) {
        DirectedGraph tmp(other);
        std::swap(tmp.graph, graph);
        std::swap(tmp.vid2label, vid2label);
        std::swap(tmp.label2vid, label2vid);
    }
    return *this;
}

DirectedGraph::~DirectedGraph() {}

DirectedGraph::DirectedGraph(const igraph_t *other) : Graph(other) {}

bool DirectedGraph::is_dag() const {
    igraph_bool_t out;
    igraph_is_dag(&graph, &out);
    return out;
}

Graph DirectedGraph::to_undirected() const {
    igraph_t undirected;
    igraph_copy(&undirected, &graph);
    igraph_to_undirected(&undirected, IGRAPH_TO_UNDIRECTED_COLLAPSE, 0);
    Graph out(&undirected);
    igraph_destroy(&undirected);
    return out;
}

Nodes DirectedGraph::parents(const Node &label) const {
    Nodes out;
    igraph_vector_t parents;
    igraph_vector_init(&parents, 1);
    igraph_neighbors(&graph, &parents, label2vid.at(label), IGRAPH_IN);
    for (int64_t i = 0; i < igraph_vector_size(&parents); i++) {
        out.push_back(vid2label[VECTOR(parents)[i]]);
    }
    igraph_vector_destroy(&parents);
    return out;
}

Nodes DirectedGraph::family(const Node &label) const {
    Nodes out = parents(label);
    out.push_back(label);
    return out;
}

Nodes DirectedGraph::children(const Node &label) const {
    Nodes out;
    igraph_vector_t children;
    igraph_vector_init(&children, 1);
    igraph_neighbors(&graph, &children, label2vid.at(label), IGRAPH_OUT);
    for (int64_t i = 0; i < igraph_vector_size(&children); i++) {
        out.push_back(vid2label[VECTOR(children)[i]]);
    }
    igraph_vector_destroy(&children);
    return out;
}

Nodes DirectedGraph::ancestors(const Node &label) const {
    std::set<Node> ancestors;
    std::list<Node> queue({label});
    while (!queue.empty()) {
        Nodes parent = parents(queue.front());
        ancestors.insert(parent.begin(), parent.end());
        queue.insert(queue.end(), parent.begin(), parent.end());
        queue.pop_front();
    }
    Nodes out(ancestors.begin(), ancestors.end());
    return out;
}

Nodes DirectedGraph::descendants(const Node &label) const {
    std::set<Node> descendants;
    std::list<Node> queue({label});
    while (!queue.empty()) {
        Nodes child = children(queue.front());
        descendants.insert(child.begin(), child.end());
        queue.insert(queue.end(), child.begin(), child.end());
        queue.pop_front();
    }
    Nodes out(descendants.begin(), descendants.end());
    return out;
}

DirectedGraph DirectedGraph::random(size_t nodes, double edge_probability) {
    igraph_t graph;
    igraph_erdos_renyi_game(
        &graph,
        IGRAPH_ERDOS_RENYI_GNP,
        nodes,
        edge_probability,
        IGRAPH_DIRECTED,
        false
    );
    DirectedGraph out(&graph);
    return out;
}

}  // namespace structures

}  // namespace madbayes