#pragma once

#include "discrete_bayesian_network.hpp"

namespace madbayes {

namespace structures {

DiscreteBayesianNetwork::DiscreteBayesianNetwork() : BayesianNetwork() {}

DiscreteBayesianNetwork::DiscreteBayesianNetwork(const std::string &formula, const CPTs &cpts) : BayesianNetwork(formula), cpts(cpts) {}

DiscreteBayesianNetwork::DiscreteBayesianNetwork(const Nodes &labels, const CPTs &cpts) : BayesianNetwork(labels), cpts(cpts) {}

DiscreteBayesianNetwork::DiscreteBayesianNetwork(const Edges &edges, const CPTs &cpts) : BayesianNetwork(edges), cpts(cpts) {}

DiscreteBayesianNetwork::DiscreteBayesianNetwork(const DiscreteBayesianNetwork &other) : BayesianNetwork(other), cpts(other.cpts) {}

DiscreteBayesianNetwork &DiscreteBayesianNetwork::operator=(const DiscreteBayesianNetwork &other) {
    if (this != &other) {
        DiscreteBayesianNetwork tmp(other);
        std::swap(tmp.graph, graph);
        std::swap(tmp.vid2label, vid2label);
        std::swap(tmp.label2vid, label2vid);
        std::swap(tmp.cpts, cpts);
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
    Coordinates axes = cpts.at(label).get_coordinates();
    auto found = std::find_if(
        axes.begin(),
        axes.end(),
        [&](const Axis &other) { return other.first == label; }
    );
    return found->second;
}

CPTs DiscreteBayesianNetwork::get_cpts() const {
    return cpts;
}

}  // namespace structures

}  // namespace madbayes
