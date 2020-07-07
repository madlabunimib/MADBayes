#pragma once

#include "graph.hpp"

namespace madbayes {

namespace structures {

void igraph_error_handler_exception(const char *reason, const char *file, int line, int igraph_errno) {
    fprintf(stderr, "Exception at %s:%i :%s, %s\n", file, line, reason, igraph_strerror(igraph_errno));
    throw std::runtime_error(reason);
}

static size_t igraph_error_handler = (size_t)igraph_set_error_handler(igraph_error_handler_exception);
static size_t igraph_attribute_table = (size_t)igraph_i_set_attribute_table(&igraph_cattribute_table);

Graph::Graph(const Nodes &labels, bool mode) {
    igraph_empty(&graph, labels.size(), mode);
    for (size_t i = 0; i < labels.size(); i++) {
        set_node_attribute(i, "label", labels[i]);
    }
    sync_nodes_labels();
}

Graph::Graph(const Graph &other) {
    igraph_copy(&graph, &other.graph);
    sync_nodes_labels();
}

Graph &Graph::operator=(const Graph &other) {
    if (this != &other) {
        Graph tmp(other);
        std::swap(tmp.graph, graph);
        std::swap(tmp.vid2label, vid2label);
        std::swap(tmp.label2vid, label2vid);
    }
    return *this;
}

Graph::~Graph() { igraph_destroy(&graph); }

Graph::Graph(const igraph_t *other) {
    igraph_copy(&graph, other);
    sync_nodes_labels();
}

Graph::Graph(const std::string &formula, bool mode) {
    Nodes nodes;
    Edges edges;

    std::regex delim("\\[|\\]|\\||\\:");
    std::regex regex("\\[(\\w+)\\]|\\[(\\w+)\\|(\\w+)([:\\w+]+)*\\]");
    auto regex_begin = std::sregex_iterator(formula.begin(), formula.end(), regex);
    auto regex_end = std::sregex_iterator();

    if (regex_begin == regex_end) throw std::runtime_error("Invalid formula string.");

    for (auto i = regex_begin; i != regex_end; ++i) {
        std::string s = i->str();
        auto match_begin = std::sregex_token_iterator(s.begin(), s.end(), delim, -1);
        auto match_end = std::sregex_token_iterator();

        std::sregex_token_iterator match_child = match_end;
        for (auto match_current = match_begin; match_current != match_end; ++match_current) {
            std::string parent = match_current->str();
            if (parent.length() > 0) {
                if (match_child == match_end) match_child = match_current;
                if (std::find(nodes.begin(), nodes.end(), parent) == nodes.end()) {
                    nodes.push_back(parent);
                }
                if (match_current != match_child) {
                    edges.push_back({parent, match_child->str()});
                }
            }
        }
    }

    igraph_empty(&graph, nodes.size(), mode);
    for (size_t i = 0; i < nodes.size(); i++) {
        set_node_attribute(i, "label", nodes[i]);
    }
    sync_nodes_labels();
    for (auto e : edges) add_edge(e.first, e.second);
}
}

void Graph::sync_nodes_labels() {
    vid2label.clear();
    label2vid.clear();
    for (size_t i = 0; i < size(); i++) {
        std::string label = std::to_string(i);
        try {
            label = get_node_attribute(i, "label");
        } catch(const std::exception& e) {
            set_node_attribute(i, "label", label);
        }
        vid2label.push_back(label);
        label2vid[label] = i;
    }
}

std::string Graph::get_node_attribute(size_t id, const std::string &key) const {
    return igraph_cattribute_VAS(&graph, key.c_str(), id);
}

void Graph::set_node_attribute(size_t id, const std::string &key, const std::string &value) {
    igraph_cattribute_VAS_set(&graph, key.c_str(), id, value.c_str());
}

Nodes Graph::get_nodes() const {
    Nodes labels;
    for (auto it = label2vid.begin(); it != label2vid.end(); ++it) {
        labels.push_back(it->first);
    }
    std::sort(labels.begin(), labels.end(), std::less<std::string>());
    return labels;
}

void Graph::set_nodes(const Nodes &labels) {
    for (size_t i = 0; i < labels.size(); i++) {
        set_node_attribute(i, "label", labels[i]);
    }
    sync_nodes_labels();
}

Edges Graph::get_edges() const {
    Edges edges;
    int from, to;
    for (int i = 0; i < igraph_ecount(&graph); i++) {
        igraph_edge(&graph, i, &from, &to);
        edges.push_back({vid2label[from], vid2label[to]});
    }
    return edges;
}

void Graph::add_node(const Node &label) {
    if (label2vid.find(label) != label2vid.end()) throw std::runtime_error("Node already exists.");
    igraph_add_vertices(&graph, 1, 0);
    set_node_attribute(size() - 1, "label", label);
    sync_nodes_labels();
}

void Graph::remove_node(const Node &label) {
    if (label2vid.find(label) == label2vid.end()) throw std::runtime_error("Node does not exist.");
    igraph_delete_vertices(&graph, igraph_vss_1(label2vid[label]));
    sync_nodes_labels();
}

void Graph::add_edge(const Node &from, const Node &to) {
    if (label2vid.find(from) == label2vid.end()) throw std::runtime_error("Node does not exist.");
    if (label2vid.find(to) == label2vid.end()) throw std::runtime_error("Node does not exist.");
    igraph_add_edge(&graph, label2vid[from], label2vid[to]);
}

void Graph::remove_edge(const Node &from, const Node &to) {
    if (label2vid.find(from) == label2vid.end()) throw std::runtime_error("Node does not exist.");
    if (label2vid.find(to) == label2vid.end()) throw std::runtime_error("Node does not exist.");
    igraph_es_t es;
    igraph_es_pairs_small(
        &es,
        is_directed(),
        label2vid[from],
        label2vid[to],
        -1
    );
    igraph_delete_edges(&graph, es);
    igraph_es_destroy(&es);
}

Graph Graph::subgraph(const Nodes &labels) const {
    igraph_t subgraph;
    igraph_vs_t select;
    igraph_vector_t nodes;
    igraph_vector_init(&nodes, labels.size());
    for (size_t i = 0; i < labels.size(); i++) {
        VECTOR(nodes)[i] = label2vid.at(labels[i]);
    }
    igraph_vs_vector(&select, &nodes);
    igraph_subgraph(&graph, &subgraph, select);
    igraph_vs_destroy(&select);
    igraph_vector_destroy(&nodes);
    Graph out(&subgraph);
    igraph_destroy(&subgraph);
    return out;
}

size_t Graph::size() const { return igraph_vcount(&graph); }

bool Graph::is_directed() const { return igraph_is_directed(&graph); }

bool Graph::is_chordal() const {
    igraph_bool_t out;
    igraph_is_chordal(&graph, 0, 0, &out, 0, 0);
    return out;
}

}  // namespace structures

}  // namespace madbayes