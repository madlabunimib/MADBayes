#pragma once

#include <igraph/igraph.h>

#include <algorithm>
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

class Graph {
   protected:
    igraph_t graph;
    std::vector<std::string> vid2label;
    std::unordered_map<std::string, size_t> label2vid;
    void sync_nodes_labels();

    std::string get_node_attribute(size_t id, const std::string &key) const;
    void set_node_attribute(size_t id, const std::string &key, const std::string &value);

   public:
    explicit Graph(const igraph_t *other);
    Graph(const Nodes &labels, bool mode = IGRAPH_UNDIRECTED);
    Graph(const Graph &other);
    Graph &operator=(const Graph &other);
    virtual ~Graph();

    void set_nodes(const Nodes &labels);
    Nodes get_nodes() const;

    Edges get_edges() const;

    void add_node(const Node &label);
    void remove_node(const Node &label);

    void add_edge(const Node &from, const Node &to);
    void remove_edge(const Node &from, const Node &to);

    Graph subgraph(const Nodes &labels);

    size_t size() const;
    bool is_directed() const;
    bool is_chordal() const;
};

}  // namespace structures

}  // namespace madbayes