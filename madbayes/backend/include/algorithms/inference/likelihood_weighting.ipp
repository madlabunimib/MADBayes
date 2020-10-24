#pragma once

#include "likelihood_weighting.hpp"

namespace madbayes {

namespace algorithms {

LikelihoodWeighting::LikelihoodWeighting(const DiscreteBayesianNetwork &model) : model(model) {
    order = topological_sorting(model);
    for (Node node : order) levels[node] = model.get_levels(node);
    generator.seed(time(NULL));
}

LikelihoodWeighting::LikelihoodWeighting(const LikelihoodWeighting &other)
    : order(other.order), levels(other.levels), model(other.model), generator(other.generator) {}

LikelihoodWeighting &LikelihoodWeighting::operator=(const LikelihoodWeighting &other) {
    if (this != &other) {
        LikelihoodWeighting tmp(other);
        std::swap(tmp.model, model);
        std::swap(tmp.order, order);
        std::swap(tmp.levels, levels);
        std::swap(tmp.generator, generator);
    }
    return *this;
}

LikelihoodWeighting::~LikelihoodWeighting() {}

std::pair<float, Evidence> LikelihoodWeighting::sample(const Evidence &evidence) {
    float weight = 1;
    Evidence sample;
    for (Node node : order) {
        DiscreteFactor cpt = model.get_cpt(node);
        xt::xarray<float> weights = cpt.get_slice(sample);
        if (evidence.find(node) != evidence.end()) {
            sample[node] = evidence.at(node);
        } else {
            std::discrete_distribution<size_t> distribution(weights.cbegin(), weights.cend());
            sample[node] = levels[node][distribution(generator)];
        }
        size_t idx = std::distance(
            levels[node].begin(),
            std::find(levels[node].begin(), levels[node].end(), sample[node])
        );
        weight *= weights(idx);
    }
    return {weight, sample};
}

std::vector<DiscreteFactor> LikelihoodWeighting::query(const Nodes &variables, const Evidence &evidence, const std::string &method, size_t size = 500) {
    std::vector<DiscreteFactor> out;

    if (method == "marginal") {
        for (Node node : variables) {
            out.push_back(DiscreteFactor({{node, levels[node]}}));
        }
    } else if (method == "joint" || method == "conditional") {
        Coordinates coordinates;
        for (Node node : variables) coordinates.push_back({node, levels[node]});
        out.push_back(DiscreteFactor(coordinates));
    } else {
        throw std::runtime_error("Method must be either 'marginal', 'joint' or 'conditional'.");
    }

    for (size_t i = 0; i < size; i++) {
        std::pair<float, Evidence> s = sample(evidence);
        for (auto j = out.begin(); j != out.end(); j++) {
            auto view = j->get_view(s.second);
            view += s.first;
        }
    }

    for (size_t i = 0; i < out.size(); i++) {
        if (method == "conditional") {
            Coordinates coord = out[i].get_coordinates();
            out[i] = out[i] / out[i].marginalize({coord[0].first});
        } else {
            out[i] = out[i].normalize();
        }
    }
    
    return out;
}

}  // namespace algorithms

}  // namespace madbayes
