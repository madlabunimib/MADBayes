#pragma once

#include <ctime>
#include <random>
#include "bayesian_network.ipp"
#include "discrete_factor.ipp"

namespace madbayes {

namespace structures {

using CPTs = std::map<Node, DiscreteFactor>;

class DiscreteBayesianNetwork : public BayesianNetwork {
   protected:
    CPTs cpts;

    std::minstd_rand generator;

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
    CPTs get_cpts() const;
    size_t size() const;

    std::pair<float, Level> sample(const Node &label, const Evidence &evidence);
};

}  // namespace structures

}  // namespace madbayes
