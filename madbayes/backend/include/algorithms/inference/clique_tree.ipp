#pragma once

#include <algorithms/structure/chain_cliques.ipp>
#include <algorithms/structure/chordal.ipp>
#include <algorithms/structure/maximal_cliques.ipp>
#include <algorithms/structure/maximum_cardinality_search.ipp>
#include <algorithms/structure/moral.ipp>

#include "clique_tree.hpp"

namespace madbayes {

namespace algorithms {

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
                clique.nodes.begin(),
                clique.nodes.end(),
                family.begin(),
                family.end()
            )) {
                // TODO: Look for invariant factor
                Factor factor = bn.get_cpt(node);
                clique.belief = (clique.belief.size() != 1) ? factor * clique.belief : factor;
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
        std::string Cj = cliques[idx];
        if (label2clique.find(Cj) == label2clique.end()) {
            add_node(Cj);
            label2clique.insert({Cj, cliques[idx]});
        }
        // Add separator
        Clique sep {true, sepset, {}};
        std::string separator = sep;
        if (label2clique.find(separator) == label2clique.end()) {
            add_node(separator);
            label2clique.insert({separator, sep});
        }
        add_edge(Cj, separator);
        // Add Ci
        std::string Ci = cliques[i];
        if (label2clique.find(Ci) == label2clique.end()) {
            add_node(Ci);
            label2clique.insert({Ci, cliques[i]});
        }
        add_edge(separator, Ci);
    }
}

Factor CliqueTree::calibrate_upward(const Node &prev, const Node &curr) {
    Factor message;
    for (Node next : neighbors(curr)) {
        if (next != prev) {
            Factor factor = calibrate_upward(curr, next);
            message = (message.size() > 1) ? factor * message : factor;
        }
    }

    Clique *clique = &label2clique[curr];
    if (message.size() > 1) clique->belief *= message;
    
    if (!clique->is_separator) {
        Nodes margin;
        Nodes sepset = clique->nodes;
        if (prev != Node()) sepset = label2clique[prev].nodes;
        std::set_difference(
            clique->nodes.begin(),
            clique->nodes.end(),
            sepset.begin(),
            sepset.end(),
            std::back_inserter(margin)
        );
        // TODO: Fix sum over axes
        // message = xt::sum(clique->belief, margin);
    }

    return message;
}

void CliqueTree::calibrate_downward(const Node &prev, const Node &curr, const Factor &message) {
    Clique *clique = &label2clique[curr];

    if (clique->is_separator) {
        Nodes margin;
        Nodes dims = message.dimension_labels();
        std::sort(dims.begin(), dims.end());
        std::set_difference(
            dims.begin(),
            dims.end(),
            clique->nodes.begin(),
            clique->nodes.end(),
            std::back_inserter(margin)
        );
        // TODO: Fix sum over axes
        // message = xt::sum(clique->belief, margin);
    }

    if (message.size() > 1) clique->belief *= message;

    for (Node next : neighbors(curr)) {
        if (next != prev) {
            // TODO: Check if third parameter is message or clique->belief
            calibrate_downward(curr, next, message);
        }
    }
}

CliqueTree::CliqueTree(const BayesianNetwork &bn) : Graph() {
    Cliques cliques = build_cliques(bn);
    build_clique_tree(cliques);

    Node root = get_nodes()[0];
    calibrate_upward(Node(), root);
    calibrate_downward(Node(), root, {});
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

Clique CliqueTree::get_clique(const Node &label) const {
    return label2clique.at(label);
}

void CliqueTree::set_clique(const Clique &clique) {
    label2clique[clique] = clique;
}

}  // namespace algorithms

}  // namespace madbayes
