#pragma once

#include "bayesian_network.ipp"

namespace madbayes {

using Level = std::string;
using Levels = std::vector<Level>;

namespace structures {

class DiscreteBayesianNetwork : public BayesianNetwork {
   public:
    DiscreteBayesianNetwork();
    explicit DiscreteBayesianNetwork(const std::string &formula, const CPTs &cpts);
    explicit DiscreteBayesianNetwork(const Nodes &labels, const CPTs &cpts);
    explicit DiscreteBayesianNetwork(const Edges &edges, const CPTs &cpts);
    DiscreteBayesianNetwork(const DiscreteBayesianNetwork &other);
    DiscreteBayesianNetwork &operator=(const DiscreteBayesianNetwork &other);
    virtual ~DiscreteBayesianNetwork();

    [[deprecated]]
    Levels get_levels(const Node &label) const;
};

}  // namespace structures

}  // namespace madbayes
