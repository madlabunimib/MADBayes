#pragma once

#include "graph.ipp"

namespace madbayes {

namespace structures {

class DirectedGraph : public Graph {
   public:
    explicit DirectedGraph(const igraph_t *other);
    explicit DirectedGraph(const std::string &formula);
    explicit DirectedGraph(const Nodes &labels);
    DirectedGraph(const Graph &other);
    DirectedGraph(const DirectedGraph &other);
    DirectedGraph &operator=(const DirectedGraph &other);
    virtual ~DirectedGraph();

    bool is_dag() const;

    Graph to_undirected();
};

}  // namespace structures

}  // namespace madbayes