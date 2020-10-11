#pragma once

#include <ctime>
#include <random>
#include <structures/discrete_bayesian_network.hpp>

namespace madbayes {

namespace algorithms {

using namespace madbayes::structures;

std::vector<Evidence> forward_sampling(const DiscreteBayesianNetwork &other, size_t size) {
    std::vector<Evidence> out;

    std::minstd_rand generator;
    generator.seed(time(NULL));

    Nodes order = topological_sorting(other);

    std::map<Node, Levels> levels;
    for (Node node : order) levels[node] = other.get_levels(node);

    for (size_t i = 0; i < size; i++) {
        Evidence sample;
        for (Node node : order) {
            DiscreteFactor cpt = other.get_cpt(node);
            xt::xarray<double> weights = cpt.get_slice(sample);
            std::discrete_distribution<size_t> distribution(weights.cbegin(), weights.cend());
            sample[node] = levels[node][distribution(generator)];
        }
        out.push_back(sample);
    }

    return out;
}

}  // namespace algorithms

}  // namespace madbayes
