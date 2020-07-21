#pragma once

#include "directed_graph.ipp"
#include "probability_table.ipp"

namespace madbayes {

using CPT = DataArray;
using CPTs = std::map<Node, CPT>;
using Level = std::string;
using Levels = std::vector<Level>;

namespace structures {

class BayesianNetwork : public DirectedGraph {
   private:
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
    void set_cpt(const Node &label, const CPT &cpt);

    [[deprecated]]
    Levels get_levels(const Node &label) const;
};

}  // namespace structures

}  // namespace madbayes
