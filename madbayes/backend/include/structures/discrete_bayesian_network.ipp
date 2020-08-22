#pragma once

#include "discrete_bayesian_network.hpp"

namespace madbayes {

namespace structures {

DiscreteBayesianNetwork::DiscreteBayesianNetwork() : BayesianNetwork() {}

DiscreteBayesianNetwork::DiscreteBayesianNetwork(const std::string &formula, const CPTs &cpts) : BayesianNetwork(formula, cpts) {}

DiscreteBayesianNetwork::DiscreteBayesianNetwork(const Nodes &labels, const CPTs &cpts) : BayesianNetwork(labels, cpts) {}

DiscreteBayesianNetwork::DiscreteBayesianNetwork(const Edges &edges, const CPTs &cpts) : BayesianNetwork(edges, cpts) {}

DiscreteBayesianNetwork::DiscreteBayesianNetwork(const DiscreteBayesianNetwork &other) : BayesianNetwork(other) {}

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

Levels DiscreteBayesianNetwork::get_levels(const Node &label) const {
    Levels coord;
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
