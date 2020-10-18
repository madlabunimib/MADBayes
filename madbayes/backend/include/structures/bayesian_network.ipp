#pragma once

#include "bayesian_network.hpp"

namespace madbayes {

namespace structures {

BayesianNetwork::BayesianNetwork() : DirectedGraph() {}

BayesianNetwork::BayesianNetwork(const std::string &formula) : DirectedGraph(formula) {}

BayesianNetwork::BayesianNetwork(const Nodes &labels) : DirectedGraph(labels) {}

BayesianNetwork::BayesianNetwork(const Edges &edges) : DirectedGraph(edges) {}

BayesianNetwork::BayesianNetwork(const BayesianNetwork &other) : DirectedGraph(other) {}

BayesianNetwork &BayesianNetwork::operator=(const BayesianNetwork &other) {
    if (this != &other) {
        BayesianNetwork tmp(other);
        std::swap(tmp.graph, graph);
        std::swap(tmp.labels, labels);
        std::swap(tmp.index, index);
    }
    return *this;
}

BayesianNetwork::~BayesianNetwork() {}

}  // namespace structures

}  // namespace madbayes
