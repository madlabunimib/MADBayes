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
        std::swap(tmp.vid2label, vid2label);
        std::swap(tmp.label2vid, label2vid);
    }
    return *this;
}

BayesianNetwork::~BayesianNetwork() {}

}  // namespace structures

}  // namespace madbayes
