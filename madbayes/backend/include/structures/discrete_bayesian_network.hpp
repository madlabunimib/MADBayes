#pragma once

#include "bayesian_network.ipp"
#include "discrete_factor.ipp"

namespace madbayes {

using Level = std::string;
using Levels = std::vector<Level>;

namespace structures {

using CPTs = std::map<Node, DiscreteFactor>;

class DiscreteBayesianNetwork : public BayesianNetwork {
   protected:
    CPTs cpts;

   public:
    DiscreteBayesianNetwork();
    explicit DiscreteBayesianNetwork(const std::string &formula, const CPTs &cpts);
    explicit DiscreteBayesianNetwork(const Nodes &labels, const CPTs &cpts);
    explicit DiscreteBayesianNetwork(const Edges &edges, const CPTs &cpts);
    DiscreteBayesianNetwork(const DiscreteBayesianNetwork &other);
    DiscreteBayesianNetwork &operator=(const DiscreteBayesianNetwork &other);
    virtual ~DiscreteBayesianNetwork();

    DiscreteFactor operator()(const Node &label) const;
    DiscreteFactor get_cpt(const Node &label) const;
    void set_cpt(const Node &label, const DiscreteFactor &cpt);

    [[deprecated]]
    Levels get_levels(const Node &label) const;
};

}  // namespace structures

}  // namespace madbayes
