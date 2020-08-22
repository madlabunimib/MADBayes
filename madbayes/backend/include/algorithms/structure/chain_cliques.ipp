#pragma once

#include <structures/graph.hpp>

namespace madbayes {

namespace algorithms {

std::vector<Nodes> chain_of_cliques(const std::vector<Nodes> &cliques, const Nodes &alpha) {
    std::vector<Nodes> out;
    std::vector<std::pair<size_t, Nodes>> chain;
    for (Nodes clique : cliques) {
        size_t max = 0;
        for (Node node : clique) {
            size_t value = std::distance(
                alpha.begin(),
                std::find(alpha.begin(), alpha.end(), node)
            );
            if (value > max) max = value;
        }
        chain.push_back({max, clique});
    }
    std::sort(chain.begin(), chain.end());
    for (auto pair : chain) out.push_back(pair.second);
    return out;
}

}  // namespace algorithms

}  // namespace madbayes