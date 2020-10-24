#pragma once

#include <ctime>
#include <random>
#include <structures/discrete_bayesian_network.hpp>

namespace madbayes {

namespace algorithms {

using namespace madbayes::structures;

std::vector<Evidence> forward_sampling(DiscreteBayesianNetwork &other, size_t size) {
    std::vector<Evidence> out;
    Nodes order = topological_sorting(other);

    for (size_t i = 0; i < size; i++) {
        Evidence sample;
        for (Node node : order) {
            sample[node] = other.sample(node, sample).second;
        }
        out.push_back(sample);
    }

    return out;
}

}  // namespace algorithms

}  // namespace madbayes
