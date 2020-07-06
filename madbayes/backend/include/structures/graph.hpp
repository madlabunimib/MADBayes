#pragma once

#include <igraph/igraph.h>

#include <algorithm>
#include <map>
#include <stdexcept>
#include <string>
#include <vector>

namespace madbayes {

namespace structures {

using Labels = std::vector<std::string>;

class Graph {
   protected:
    igraph_t graph;
    std::map<std::string, size_t> labels;

   public:
    explicit Graph(const igraph_t *other);
    Graph(const Labels &labels, bool mode = IGRAPH_UNDIRECTED);
    Graph(const Graph &other);
    Graph &operator=(const Graph &other);
    virtual ~Graph();

    Labels get_labels() const;
    void set_labels(const Labels &label);

    void add_vertex(const std::string &label);
    void remove_vertex(const std::string &label);

    void add_edge(const std::string &from, const std::string &to);
    void remove_edge(const std::string &from, const std::string &to);

    size_t size() const;
    bool is_directed() const;
    bool is_chordal() const;
};

}  // namespace structures

}  // namespace madbayes