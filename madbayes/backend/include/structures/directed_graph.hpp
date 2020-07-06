#pragma once

#include "graph.ipp"

namespace madbayes {

namespace structures {

class DirectedGraph : public Graph {
   public:
    explicit DirectedGraph(int64_t nodes);
    DirectedGraph(const DirectedGraph &other);
    DirectedGraph &operator=(const DirectedGraph &other);
    virtual ~DirectedGraph();

    bool is_dag() const;
};

}  // namespace structures

}  // namespace madbayes