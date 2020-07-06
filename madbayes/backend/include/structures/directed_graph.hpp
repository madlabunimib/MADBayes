#pragma once

#include "graph.ipp"

namespace madbayes {

namespace structures {

class DirectedGraph : public Graph {
   public:
    explicit DirectedGraph(const igraph_t *other);
    explicit DirectedGraph(int64_t nodes);
    DirectedGraph(const DirectedGraph &other);
    DirectedGraph &operator=(const DirectedGraph &other);
    virtual ~DirectedGraph();

    bool is_dag() const;

    Graph to_undirected();
};

}  // namespace structures

}  // namespace madbayes