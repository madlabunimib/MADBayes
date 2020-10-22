#pragma once

#include "likelihood_weighting.hpp"

namespace madbayes {

namespace algorithms {

LikelihoodWeighting::LikelihoodWeighting(const DiscreteBayesianNetwork &model) : model(model) {
    order = topological_sorting(model);
    for (Node node : order) levels[node] = model.get_levels(node);
}

LikelihoodWeighting::LikelihoodWeighting(const LikelihoodWeighting &other)
    : model(other.model), order(other.order), levels(other.levels) {}

LikelihoodWeighting &LikelihoodWeighting::operator=(const LikelihoodWeighting &other) {
    if (this != &other) {
        LikelihoodWeighting tmp(other);
        std::swap(tmp.model, model);
        std::swap(tmp.order, order);
        std::swap(tmp.levels, levels);
    }
    return *this;
}

LikelihoodWeighting::~LikelihoodWeighting() {}

std::vector<DiscreteFactor> LikelihoodWeighting::query(const Nodes &variables, const Evidence &evidence, const std::string &method, size_t size = 500) {
    std::vector<DiscreteFactor> out;
    std::vector<std::pair<float, Evidence>> samples;

    std::minstd_rand generator;
    generator.seed(time(NULL));

    for (size_t i = 0; i < size; i++) {
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
        samples.push_back({weight, sample});
    }

    if (method == "marginal") {
        for (Node node : variables) {
            out.push_back(DiscreteFactor({{node, levels[node]}}));
        }
    } else {
        Coordinates coordinates;
        for (Node node : variables) coordinates.push_back({node, levels[node]});
        out.push_back(DiscreteFactor(coordinates));
    }

    for (size_t i = 0; i < out.size(); i++) {
        auto j = samples.begin();
        for (; j != samples.end(); j++) {
            auto view = out[i].get_view(j->second);
            view += j->first;
        }
        out[i] = out[i].normalize();
    }
    
    return out;
}

}  // namespace algorithms

}  // namespace madbayes
