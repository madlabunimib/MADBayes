#pragma once

#include "directed_graph.ipp"
#include "probability_table.ipp"

namespace madbayes {

using CPT = DataArray;
using CPTs = std::map<Node, CPT>;
using Evidence = std::map<Node, std::string>;

namespace structures {

class BayesianNetwork : public DirectedGraph {
   protected:
    CPTs cpts;

   public:
    BayesianNetwork();
    explicit BayesianNetwork(const std::string &formula, const CPTs &cpts);
    explicit BayesianNetwork(const Nodes &labels, const CPTs &cpts);
    explicit BayesianNetwork(const Edges &edges, const CPTs &cpts);
    BayesianNetwork(const BayesianNetwork &other);
    BayesianNetwork &operator=(const BayesianNetwork &other);
    virtual ~BayesianNetwork();

    CPT operator()(const Node &label) const;
    CPT get_cpt(const Node &label) const;
    void set_cpt(const Node &label, const CPT &cpt);
};

}  // namespace structures

}  // namespace madbayes
