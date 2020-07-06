#pragma once

#include <igraph/igraph.h>

#include <algorithm>
#include <map>
#include <stdexcept>
#include <string>
#include <vector>

namespace madbayes {

namespace structures {

class Graph {
   protected:
    igraph_t graph;
    std::map<std::string, size_t> nodes;

   public:
    explicit Graph(const igraph_t *other);
    Graph(const std::vector<std::string> &nodes, bool mode = IGRAPH_UNDIRECTED);
    Graph(const Graph &other);
    Graph &operator=(const Graph &other);
    virtual ~Graph();

    size_t size() const;
    bool is_directed() const;
    bool is_chordal() const;
};

}  // namespace structures

}  // namespace madbayes