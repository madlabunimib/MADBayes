#pragma once

#include "bayesian_network.ipp"
#include "data_array.ipp"

namespace madbayes {

namespace structures {

using CPT = DataArray;
using CPTs = std::map<Node, CPT>;

using Level = std::string;
using Levels = std::vector<Level>;

using Evidence = std::map<Node, std::string>;

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

    CPT operator()(const Node &label) const;
    CPT get_cpt(const Node &label) const;
    void set_cpt(const Node &label, const CPT &cpt);

    [[deprecated]]
    Levels get_levels(const Node &label) const;
};

}  // namespace structures

}  // namespace madbayes
