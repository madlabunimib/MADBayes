#pragma once

#include "bayesian_network.hpp"

namespace madbayes {

namespace structures {

BayesianNetwork::BayesianNetwork() : DirectedGraph() {}

BayesianNetwork::BayesianNetwork(const std::string &formula, const CPTs &cpts) : DirectedGraph(formula), cpts(cpts) {}

BayesianNetwork::BayesianNetwork(const Nodes &labels, const CPTs &cpts) : DirectedGraph(labels), cpts(cpts) {}

BayesianNetwork::BayesianNetwork(const Edges &edges, const CPTs &cpts) : DirectedGraph(edges), cpts(cpts) {}

BayesianNetwork::BayesianNetwork(const BayesianNetwork &other) : DirectedGraph(other), cpts(other.cpts) {}

BayesianNetwork &BayesianNetwork::operator=(const BayesianNetwork &other) {
    if (this != &other) {
        BayesianNetwork tmp(other);
        std::swap(tmp.graph, graph);
        std::swap(tmp.vid2label, vid2label);
        std::swap(tmp.label2vid, label2vid);
        std::swap(tmp.cpts, cpts);
    }
    return *this;
}

BayesianNetwork::~BayesianNetwork() {}

CPT BayesianNetwork::operator()(const Node &label) const {
    return cpts.at(label);
}

void BayesianNetwork::set_cpt(const Node &label, const CPT &cpt) {
    cpts[label] = cpt;
}

std::vector<std::string> BayesianNetwork::get_levels(const Node &label) const {
    std::vector<std::string> coord;
    auto _coord = cpts.at(label).coordinates();
    for (auto i = _coord.begin(); i != _coord.end(); ++i) {
        if (i->first == label) {
            size_t end = i->second.labels().size();
            auto _labels = i->second.labels().data();
            for (auto j = _labels; j < _labels + end; ++j) {
                coord.push_back(*j);
            }
            return coord;
        }
    }
    return coord;
}

}  // namespace structures

}  // namespace madbayes
