#pragma once

#include "graph.hpp"

namespace madbayes {

namespace structures {

void igraph_error_handler_exception(const char *reason, const char *file, int line, int igraph_errno) {
    std::ostringstream out;
    out << "Exception at " << file << ":" << line << " :";
    out << reason << ", " << igraph_strerror(igraph_errno) << "\n";
    throw std::runtime_error(out.str());
}

static size_t igraph_error_handler = (size_t)igraph_set_error_handler(igraph_error_handler_exception);
static size_t igraph_attribute_table = (size_t)igraph_i_set_attribute_table(&igraph_cattribute_table);

Graph::Graph() { igraph_empty(&graph, 0, IGRAPH_UNDIRECTED); }

Graph::Graph(const Nodes &labels, bool mode) {
    igraph_empty(&graph, labels.size(), mode);
    for (size_t i = 0; i < labels.size(); i++) {
        set_node_attribute(i, "label", labels[i]);
    }
    sync_nodes_labels();
}

Graph::Graph(const Edges &edges, bool mode) {
    if (edges.size() == 0) throw std::runtime_error("Edge list cannot be empty.");

    std::set<Node> nodes;
    for (Edge e : edges) {
        nodes.insert(e.first);
        nodes.insert(e.second);
    }

    igraph_empty(&graph, nodes.size(), mode);

    size_t i = 0;
    for (Node n: nodes) {
        set_node_attribute(i, "label", n);
        i++;
    }

    sync_nodes_labels();
    
    for (Edge e : edges) add_edge(e.first, e.second);
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

void Graph::sync_nodes_labels() {
    vid2label.clear();
    label2vid.clear();
    for (size_t i = 0; i < size(); i++) {
        std::string label;
        try {
            label = get_node_attribute(i, "label");
            if (label.size() <= 0) throw std::runtime_error("Invalid node label.");
        } catch(const std::exception& e) {
            label = std::to_string(i);
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
    return vid2label;
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

bool Graph::has_node(const Node &label) const {
    return label2vid.find(label) != label2vid.end();
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

bool Graph::has_edge(const Node &from, const Node &to) const {
    int edge;
    if (label2vid.find(from) == label2vid.end()) throw std::runtime_error("Node does not exist.");
    if (label2vid.find(to) == label2vid.end()) throw std::runtime_error("Node does not exist.");
    igraph_get_eid(&graph, &edge, label2vid.at(from), label2vid.at(to), is_directed(), false);
    return edge >= 0;
}

void Graph::add_edge(const Node &from, const Node &to) {
    if (label2vid.find(from) == label2vid.end()) throw std::runtime_error("Node does not exist.");
    if (label2vid.find(to) == label2vid.end()) throw std::runtime_error("Node does not exist.");
    if (!has_edge(from, to)) igraph_add_edge(&graph, label2vid[from], label2vid[to]);
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

Nodes Graph::neighbors(const Node &label) const {
    Nodes out;
    igraph_vector_t neighbors;
    igraph_vector_init(&neighbors, 1);
    igraph_neighbors(&graph, &neighbors, label2vid.at(label), IGRAPH_ALL);
    for (int64_t i = 0; i < igraph_vector_size(&neighbors); i++) {
        out.push_back(vid2label[VECTOR(neighbors)[i]]);
    }
    igraph_vector_destroy(&neighbors);
    return out;
}

Nodes Graph::boundary(const Nodes &labels) const {
    Nodes out;
    std::set<Node> boundary;
    for (Node bound : labels)
        for (Node neighbor : neighbors(bound))
            boundary.insert(neighbor);
    std::set_difference(
        boundary.begin(),
        boundary.end(),
        labels.begin(),
        labels.end(),
        std::inserter(out, out.begin())
    );
    return out;
}

FILE *Graph::open_dot_file() const {
    FILE *out = std::tmpfile();
    igraph_write_graph_dot(&graph, out);
    rewind(out);
    return out;
}

std::string Graph::__repr__() const {
    size_t size;
    char *buffer;
    std::stringstream out;
    FILE *tmp = open_dot_file();
    if (tmp) {
        fseek(tmp, 0, SEEK_END);
        size = ftell(tmp);
        fseek(tmp, 0, SEEK_SET);
        buffer = (char *) malloc(size);
        if (buffer) size = fread(buffer, 1, size, tmp);
        fclose(tmp);
    }
    if (buffer) {
        out << buffer;
        free(buffer);
    }
    return out.str();
}

Graph Graph::random(size_t nodes, double edge_probability) {
    igraph_t graph;
    igraph_erdos_renyi_game(
        &graph,
        IGRAPH_ERDOS_RENYI_GNP,
        nodes,
        edge_probability,
        IGRAPH_UNDIRECTED,
        false
    );
    Graph out(&graph);
    return out;
}

}  // namespace structures

}  // namespace madbayes