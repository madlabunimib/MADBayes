#pragma once

#include <random>
#include <structures/discrete_bayesian_network.hpp>

namespace madbayes {

namespace algorithms {

using namespace madbayes::structures;

class LikelihoodWeighting {
   private:
    // TODO: Remove this pointer
    const DiscreteBayesianNetwork *other;

    size_t size;
    Nodes sorting;
    std::default_random_engine generator;
    std::uniform_real_distribution<double> uniform;

   public:
    LikelihoodWeighting(const DiscreteBayesianNetwork &other, size_t size);
    LikelihoodWeighting(const LikelihoodWeighting &other);
    LikelihoodWeighting &operator=(const LikelihoodWeighting &other);
    ~LikelihoodWeighting();

    std::vector<DiscreteFactor> query(const Nodes &variables, const Evidence &evidence, const std::string &method);
};

}  // namespace algorithms

}  // namespace madbayes