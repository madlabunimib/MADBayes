#pragma once

#include "graph.ipp"

namespace madbayes {

namespace structures {

class DirectedGraph : public Graph {
   public:
    explicit DirectedGraph(const igraph_t *other);
    explicit DirectedGraph(const std::string &formula);
    explicit DirectedGraph(const Nodes &labels);
    explicit DirectedGraph(const Edges &edges);
    DirectedGraph(const Graph &other);
    DirectedGraph(const DirectedGraph &other);
    DirectedGraph &operator=(const DirectedGraph &other);
    virtual ~DirectedGraph();

    bool is_dag() const;

    Graph to_undirected();

    Nodes parents(const Node &label) const;
    Nodes family(const Node &label) const;
    Nodes children(const Node &label) const;
    Nodes ancestors(const Node &label) const;
    Nodes descendants(const Node &label) const;
};

}  // namespace structures

}  // namespace madbayes