#pragma once

#include "directed_graph.ipp"

namespace madbayes {

namespace structures {

class BayesianNetwork : public DirectedGraph {

   public:
    BayesianNetwork();
    explicit BayesianNetwork(const std::string &formula);
    explicit BayesianNetwork(const Nodes &labels);
    explicit BayesianNetwork(const Edges &edges);
    BayesianNetwork(const BayesianNetwork &other);
    BayesianNetwork &operator=(const BayesianNetwork &other);
    virtual ~BayesianNetwork();
};

}  // namespace structures

}  // namespace madbayes
