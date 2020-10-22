#pragma once

#include <ctime>
#include <random>
#include <structures/discrete_bayesian_network.hpp>

namespace madbayes {

namespace algorithms {

using namespace madbayes::structures;

class LikelihoodWeighting {
   private:
    DiscreteBayesianNetwork model;

    Nodes order;
    std::map<Node, Levels> levels;

   public:
    LikelihoodWeighting(const DiscreteBayesianNetwork &other);
    LikelihoodWeighting(const LikelihoodWeighting &other);
    LikelihoodWeighting &operator=(const LikelihoodWeighting &other);
    ~LikelihoodWeighting();

    std::vector<DiscreteFactor> query(const Nodes &variables, const Evidence &evidence, const std::string &method, size_t size);
};

}  // namespace algorithms

}  // namespace madbayes