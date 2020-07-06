#pragma once

#include <igraph/igraph.h>

#include <algorithm>
#include <stdexcept>

namespace madbayes {

namespace structures {

class Graph {
   protected:
    igraph_t graph;

   public:
    explicit Graph(int64_t nodes);
    Graph(const Graph &other);
    Graph &operator=(const Graph &other);
    ~Graph();

    size_t size() const;
};

}  // namespace structures

}  // namespace madbayes