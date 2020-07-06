#pragma once

#include <igraph/igraph.h>

#include <algorithm>
#include <stdexcept>

namespace madbayes {

namespace structures {

class Graph {
   protected:
    igraph_t graph;

    Graph();

   public:
    explicit Graph(const igraph_t *other);
    Graph(int64_t nodes, bool mode = IGRAPH_UNDIRECTED);
    Graph(const Graph &other);
    Graph &operator=(const Graph &other);
    virtual ~Graph();

    size_t size() const;
    bool is_directed() const;
    bool is_chordal() const;
};

}  // namespace structures

}  // namespace madbayes