#pragma once

#include "discrete_bayesian_network.hpp"

namespace madbayes {

namespace structures {

DiscreteBayesianNetwork::DiscreteBayesianNetwork() : BayesianNetwork() {
    generator.seed(time(NULL));
}

DiscreteBayesianNetwork::DiscreteBayesianNetwork(const std::string &formula, const CPTs &cpts) : BayesianNetwork(formula), cpts(cpts) {
    generator.seed(time(NULL));
}

DiscreteBayesianNetwork::DiscreteBayesianNetwork(const Nodes &labels, const CPTs &cpts) : BayesianNetwork(labels), cpts(cpts) {
    generator.seed(time(NULL));
}

DiscreteBayesianNetwork::DiscreteBayesianNetwork(const Edges &edges, const CPTs &cpts) : BayesianNetwork(edges), cpts(cpts) {
    generator.seed(time(NULL));
}

DiscreteBayesianNetwork::DiscreteBayesianNetwork(const DiscreteBayesianNetwork &other)
    : BayesianNetwork(other), cpts(other.cpts), generator(other.generator) {}

DiscreteBayesianNetwork &DiscreteBayesianNetwork::operator=(const DiscreteBayesianNetwork &other) {
    if (this != &other) {
        DiscreteBayesianNetwork tmp(other);
        std::swap(tmp.graph, graph);
        std::swap(tmp.labels, labels);
        std::swap(tmp.index, index);
        std::swap(tmp.cpts, cpts);
        std::swap(tmp.generator, generator);
    }
    return *this;
}

DiscreteBayesianNetwork::~DiscreteBayesianNetwork() {}

DiscreteFactor DiscreteBayesianNetwork::operator()(const Node &label) const {
    return cpts.at(label);
}

DiscreteFactor DiscreteBayesianNetwork::get_cpt(const Node &label) const {
    return cpts.at(label);
}

void DiscreteBayesianNetwork::set_cpt(const Node &label, const DiscreteFactor &cpt) {
    cpts[label] = cpt;
}

Levels DiscreteBayesianNetwork::get_levels(const Node &label) const {
    return cpts.at(label).get_levels(label);
}

CPTs DiscreteBayesianNetwork::get_cpts() const {
    return cpts;
}

size_t DiscreteBayesianNetwork::size() const {
    size_t out = 0;
    Nodes nodes = get_nodes();
    std::map<Node, size_t> levels_count;

    for (const Node &node : nodes) {
        levels_count[node] = get_levels(node).size();
    }

    for (const Node &node : nodes) {
        size_t counter = levels_count[node] - 1;
        for (const Node &parent : parents(node)) {
            counter *= levels_count[parent];
        }
        out += counter;
    }

    return out;
}

std::pair<float, Level> DiscreteBayesianNetwork::sample(const Node &label, const Evidence &evidence) {
    DiscreteFactor *cpt = &cpts.at(label);
    xt::xarray<float> weights = cpt->get_slice(evidence);
    std::discrete_distribution<size_t> distribution(weights.begin(), weights.end());
    size_t idx = distribution(generator);
    return {weights(idx), cpt->get_level(label, idx)};
}

}  // namespace structures

}  // namespace madbayes
