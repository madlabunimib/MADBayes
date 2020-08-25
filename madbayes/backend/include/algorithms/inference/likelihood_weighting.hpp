#pragma once

#include <random>
#include <structures/bayesian_network.hpp>
#include <structures/discrete_bayesian_network.hpp>

namespace madbayes {

namespace algorithms {

using namespace madbayes::structures;

class LikelihoodWeighting {
   private:
    // TODO: Remove this pointer
    const BayesianNetwork *bn;

    size_t samples;
    Nodes sorting;
    std::default_random_engine generator;
    std::uniform_real_distribution<double> uniform;

   public:
    LikelihoodWeighting(const BayesianNetwork &other, size_t n_samples);
    LikelihoodWeighting(const LikelihoodWeighting &other);
    LikelihoodWeighting &operator=(const LikelihoodWeighting &other);
    ~LikelihoodWeighting();

    std::vector<DataArray> query(const Nodes &variables, const Evidence &evidence, const std::string &method);
};

}  // namespace algorithms

}  // namespace madbayes