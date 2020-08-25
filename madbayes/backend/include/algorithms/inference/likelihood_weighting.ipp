#pragma once

#include <algorithms/structure/topological_sorting.ipp>

#include "likelihood_weighting.hpp"

namespace madbayes {

namespace algorithms {

LikelihoodWeighting::LikelihoodWeighting(const BayesianNetwork &other, size_t samples) : bn(&other), samples(samples) {
    sorting = topological_sorting(other);
    uniform = std::uniform_real_distribution<double>(0.0, 1.0);
}

LikelihoodWeighting::LikelihoodWeighting(const LikelihoodWeighting &other)
    : samples(other.samples), sorting(other.sorting), generator(other.generator), uniform(other.uniform) {}

LikelihoodWeighting &LikelihoodWeighting::operator=(const LikelihoodWeighting &other) {
    if (this != &other) {
        LikelihoodWeighting tmp(other);
        std::swap(tmp.bn, bn);
        std::swap(tmp.samples, samples);
        std::swap(tmp.sorting, sorting);
        std::swap(tmp.generator, generator);
        std::swap(tmp.uniform, uniform);
    }
    return *this;
}

LikelihoodWeighting::~LikelihoodWeighting() {}

std::vector<DataArray> LikelihoodWeighting::query(const Nodes &variables, const Evidence &evidence,
                                                  const std::string &method) {
    std::vector<DataArray> out;
    
    if (method == "marginal") {
        for (Node node : variables) {
            
        }
    } else if (method == "joint" || method == "conditional") {

    } else {
        throw std::runtime_error("'method' must be 'marginal', 'joint' or 'conditional'.");
    }
    
    for (size_t i = 0; i < samples; i++) {
        // TODO: Get Evidence type from bn type
        Evidence sample;
        double weight = 1;
        for (Node Xi : sorting) {
            // TODO: Refactor xf::select to use std::map as index
            CPT table = bn->get_cpt(Xi);
            for (auto it = sample.begin(); it != sample.end(); i++) {
                auto dims = table.dimension_labels();
                if (std::find(dims.begin(), dims.end(), it->first) != dims.end()) {
                    table = xf::select(table, {{it->first, it->second}});
                }
            }

            if (evidence.find(Xi) == evidence.end()) {
                size_t index = 0;
                double cumulative = 0;
                while (uniform(generator) > cumulative) {
                    cumulative += table(index).value();
                    index++;
                }
                // TODO: Generalize to non-discrete bn
                sample[Xi] = ((DiscreteBayesianNetwork *) (bn))->get_levels(Xi)[i];
            } else {
                sample[Xi] = evidence.at(Xi);
                weight *= table.locate(evidence.at(Xi)).value();
            }

        }
    }
}

}  // namespace algorithms

}  // namespace madbayes
