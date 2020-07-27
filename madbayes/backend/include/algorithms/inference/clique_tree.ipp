#pragma once

#include <algorithms/structure/chain_cliques.ipp>
#include <algorithms/structure/chordal.ipp>
#include <algorithms/structure/maximal_cliques.ipp>
#include <algorithms/structure/maximum_cardinality_search.ipp>
#include <algorithms/structure/moral.ipp>

#include "clique_tree.hpp"

namespace madbayes {

namespace algorithms {

std::string CliqueTree::clique2label(const Clique &clique) {
    std::stringstream out;
    if (clique.nodes.empty()) {
        throw std::runtime_error("Empty clique has no label.");
    }
    out << '[' << clique.nodes[0];
    for (size_t i = 1; i < clique.nodes.size(); i++) {
        out << '_' << clique.nodes[i];
    }
    out << ']';
    return out.str();
}

Cliques CliqueTree::build_cliques(const BayesianNetwork &bn) {
    Graph moral_graph = moral(bn);
    Graph chordal_graph = chordal(moral_graph);
    std::vector<Nodes> cliques = maximal_cliques(chordal_graph);
    Nodes alpha = maximum_cardinality_search(chordal_graph);
    std::vector<Nodes> chain = chain_of_cliques(cliques, alpha);

    // Assign CPTs to clique
    Cliques out;
    Nodes nodes = bn.get_nodes();
    for (size_t i = 0; i < chain.size(); i++) {
        std::sort(chain[i].begin(), chain[i].end());
        Clique clique {false, chain[i], {}};
        for (Node node : nodes) {
            Nodes family = bn.family(node);
            std::sort(family.begin(), family.end());
            if (std::includes(
                family.begin(),
                family.end(),
                clique.nodes.begin(),
                clique.nodes.end()
            )) {
                // TODO: Search invariant factor
                auto cpt = bn.get_cpt(node);
                if (clique.belief.size() == 1) {
                    clique.belief = cpt;
                } else {
                    clique.belief *= cpt;
                }
            }
        }
        // TODO: Refactor using set_difference or incremental removal
        for (Node node : clique.nodes) {
            auto remove = std::find(nodes.begin(), nodes.end(), node);
            if (remove != nodes.end()) nodes.erase(remove);
        }
        out.push_back(clique);
    }
    return out;
}

void CliqueTree::build_clique_tree(const Cliques &cliques) {
    // Build clique tree
    for (size_t i = 1; i < cliques.size(); i++) {
        Nodes sepset;
        size_t idx = 0;
        for (size_t j = 0; j < i; j++) {
            Nodes intersect;
            std::set_intersection(
                cliques[i].nodes.begin(),
                cliques[i].nodes.end(),
                cliques[j].nodes.begin(),
                cliques[j].nodes.end(),
                std::back_inserter(intersect)
            );
            if (intersect.size() > sepset.size()) {
                sepset = intersect;
                idx = j;
            }
        }
        // Add Cj
        std::string Cj = clique2label(cliques[idx]);
        if (label2clique.find(Cj) == label2clique.end()) {
            add_node(Cj);
            label2clique.insert({Cj, cliques[idx]});
        }
        // Add separator
        Clique sep {true, sepset, {}};
        std::string separator = clique2label(sep);
        if (label2clique.find(separator) == label2clique.end()) {
            add_node(separator);
            label2clique.insert({separator, sep});
        }
        add_edge(Cj, separator);
        // Add Ci
        std::string Ci = clique2label(cliques[i]);
        if (label2clique.find(Ci) == label2clique.end()) {
            add_node(Ci);
            label2clique.insert({Ci, cliques[i]});
        }
        add_edge(separator, Ci);
    }
}

CliqueTree::CliqueTree(const BayesianNetwork &bn) : Graph() {
    Cliques cliques = build_cliques(bn);
    build_clique_tree(cliques);
}

CliqueTree::CliqueTree(const CliqueTree &other) : Graph(other), label2clique(other.label2clique) {}

CliqueTree &CliqueTree::operator=(const CliqueTree &other) {
    if (this != &other) {
        CliqueTree tmp(other);
        std::swap(tmp.graph, graph);
        std::swap(tmp.vid2label, vid2label);
        std::swap(tmp.label2vid, label2vid);
        std::swap(tmp.label2clique, label2clique);
    }
    return *this;
}

CliqueTree::~CliqueTree() {}

}  // namespace algorithms

}  // namespace madbayes
