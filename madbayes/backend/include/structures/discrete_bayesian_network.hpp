#pragma once

#include "bayesian_network.ipp"
#include "data_array.ipp"

namespace madbayes {

using Level = std::string;
using Levels = std::vector<Level>;

using Evidence = std::map<Node, std::string>;

namespace structures {

using CPTs = std::map<Node, DataArray>;

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

    DataArray operator()(const Node &label) const;
    DataArray get_cpt(const Node &label) const;
    void set_cpt(const Node &label, const DataArray &cpt);

    [[deprecated]]
    Levels get_levels(const Node &label) const;
};

}  // namespace structures

}  // namespace madbayes
