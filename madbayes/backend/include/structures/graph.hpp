#pragma once

#include <igraph/igraph.h>

#include <algorithm>
#include <cstdio>
#include <cstdlib>
#include <iostream>
#include <list>
#include <regex>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

namespace madbayes {

namespace structures {

using Node = std::string;
using Nodes = std::vector<Node>;
using Edge = std::pair<std::string, std::string>;
using Edges = std::vector<Edge>;

class DirectedGraph;

class Graph {
    friend DirectedGraph;

   private:
    FILE *open_dot_file() const;

   protected:
    igraph_t graph;
    std::vector<std::string> vid2label;
    std::unordered_map<std::string, size_t> label2vid;
    void sync_nodes_labels();

    std::string get_node_attribute(size_t id, const std::string &key) const;
    void set_node_attribute(size_t id, const std::string &key, const std::string &value);

    explicit Graph(const igraph_t *other);

   public:
    Graph();
    Graph(const std::string &formula, bool mode = IGRAPH_UNDIRECTED);
    Graph(const Nodes &labels, bool mode = IGRAPH_UNDIRECTED);
    Graph(const Edges &edges, bool mode = IGRAPH_UNDIRECTED);
    Graph(const Graph &other);
    Graph &operator=(const Graph &other);
    virtual ~Graph();

    void set_nodes(const Nodes &labels);
    Nodes get_nodes() const;

    Edges get_edges() const;

    bool has_node(const Node &label) const;
    void add_node(const Node &label);
    void remove_node(const Node &label);

    bool has_edge(const Node &from, const Node &to) const;
    void add_edge(const Node &from, const Node &to);
    void remove_edge(const Node &from, const Node &to);

    Graph subgraph(const Nodes &labels) const;

    size_t size() const;
    bool is_directed() const;
    bool is_chordal() const;

    Nodes neighbors(const Node &label) const;
    Nodes boundary(const Nodes &labels) const;

    template <typename T>
    friend T chordal(const T &other);

    std::string __repr__() const;
};

}  // namespace structures

}  // namespace madbayes