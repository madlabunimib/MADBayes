#pragma once

#include <igraph/igraph.h>

#include <algorithm>
#include <stdexcept>

namespace madbayes {

namespace structures {

class Graph {
   protected:
    Graph();
    igraph_t graph;

   public:
    Graph(int64_t nodes, bool mode = IGRAPH_UNDIRECTED);
    Graph(const Graph &other);
    Graph &operator=(const Graph &other);
    virtual ~Graph();

    size_t size() const;
    bool is_directed() const;
};

}  // namespace structures

}  // namespace madbayes