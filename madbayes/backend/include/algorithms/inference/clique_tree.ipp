#pragma once

#include "clique_tree.hpp"

namespace madbayes {

namespace algorithms {

template <typename T>
Cliques CliqueTree::build_cliques(const T &other) const {
    Graph moral_graph = moral(other);
    Graph chordal_graph = chordal(moral_graph);
    std::vector<Nodes> cliques = maximal_cliques(chordal_graph);
    Nodes alpha = maximum_cardinality_search(chordal_graph);
    std::vector<Nodes> chain = chain_of_cliques(cliques, alpha);

    // Assign CPTs to clique
    Cliques out;
    Nodes nodes = other.get_nodes();
    for (size_t i = 0; i < chain.size(); i++) {
        std::sort(chain[i].begin(), chain[i].end());
        Clique clique {false, chain[i], {}};
        for (auto node = nodes.begin(); node != nodes.end(); node++) {
            Nodes family = other.family(*node);
            std::sort(family.begin(), family.end());
            if (std::includes(
                clique.nodes.begin(),
                clique.nodes.end(),
                family.begin(),
                family.end()
            )) {
                clique.belief *= other.get_cpt(*node);
                nodes.erase(node--);
            }
        }
        out.push_back(clique);
    }
    return out;
}

void CliqueTree::build_clique_tree(const Cliques &cliques) {
    // Build clique tree
    auto i = cliques.begin() + 1;
    for (; i != cliques.end(); i++) {
        Nodes sepset;
        auto j = cliques.begin();
        auto k = cliques.begin();
        for (; j < i; j++) {
            Nodes intersect;
            std::set_intersection(
                i->nodes.begin(),
                i->nodes.end(),
                j->nodes.begin(),
                j->nodes.end(),
                std::back_inserter(intersect)
            );
            if (intersect.size() > sepset.size()) {
                sepset = intersect; k = j;
            }
        }
        // Add Cj
        std::string Cj = *k;
        if (label2clique.find(Cj) == label2clique.end()) {
            add_node(Cj);
            label2clique.insert({Cj, *k});
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
        std::string Ci = *i;
        if (label2clique.find(Ci) == label2clique.end()) {
            add_node(Ci);
            label2clique.insert({Ci, *i});
        }
        add_edge(separator, Ci);
    }
}

DiscreteFactor CliqueTree::calibrate_upward(const Node &prev, const Node &curr) {
    DiscreteFactor message;
    for (Node next : neighbors(curr)) {
        if (next != prev) {
            message *= calibrate_upward(curr, next);
        }
    }

    Clique *clique = &label2clique.at(curr);
    
    if (clique->is_separator) {
        clique->belief = message;
        return message;
    }

    clique->belief *= message;

    if (prev != Node()) {
        Nodes scope = label2clique[prev].nodes;
        message = clique->belief.marginalize(scope);
    }

    return message;
}

void CliqueTree::calibrate_downward(const Node &prev, const Node &curr, DiscreteFactor message) {
    Clique *clique = &label2clique.at(curr);

    if (clique->is_separator) {
        message = message.marginalize(clique->nodes);
        message /= clique->belief;
    }

    clique->belief *= message;

    if (!clique->is_separator) message = clique->belief;

    for (Node next : neighbors(curr)) {
        if (next != prev) {
            calibrate_downward(curr, next, message);
        }
    }
}

template <typename T>
CliqueTree::CliqueTree(const T &other) : Graph() {
    Cliques cliques = build_cliques(other);
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

void CliqueTree::absorb_evidence(const Evidence &evidence) {
    auto i = evidence.begin();
    for (; i != evidence.end(); i++) {
        Clique clique = get_clique_given_variables({i->first});
        DiscreteFactor old_margin = clique.belief.marginalize({i->first});
        DiscreteFactor new_margin = DiscreteFactor::zeros_like(old_margin);
        new_margin.set_value({*i}, 1);
        clique.belief /= old_margin;
        clique.belief *= new_margin;
        set_clique(clique);
        calibrate_downward(Node(), clique, {});
    }
}

std::vector<DiscreteFactor> CliqueTree::query(const Nodes &variables, const Evidence &evidence, const std::string &method) const {
    CliqueTree copy = CliqueTree(*this);
    copy.absorb_evidence(evidence);

    std::vector<DiscreteFactor> out;

    if (method == "marginal") {
        for (Node variable : variables) {
            DiscreteFactor marginal = copy.get_clique_given_variables({variable}).belief;
            out.push_back(marginal.marginalize({variable}));
        }
        return out;
    }
    if (method == "joint" || method == "conditional") {
        DiscreteFactor joint;

        try {
            joint = copy.get_clique_given_variables(variables).belief;
        } catch(const std::exception& e) {
            Nodes scope = Nodes(variables.begin(), variables.end());
            joint = copy.get_joint_query("", get_nodes()[0], &scope);
        }

        joint = joint.marginalize(variables);

        if (method == "joint") {
            out.push_back(joint);
            return out;
        }

        Nodes scope = Nodes(variables.begin() + 1, variables.end());
        out.push_back(joint / joint.sum(scope));
        return out;
    }

    throw std::runtime_error("Method must be either 'marginal', 'joint' or 'conditional'.");
}

Clique CliqueTree::get_clique(const Node &label) const {
    return label2clique.at(label);
}

void CliqueTree::set_clique(const Clique &clique) {
    label2clique[clique] = clique;
}

Clique CliqueTree::get_clique_given_variables(const Nodes &variables) const {
    Nodes nodes = variables;
    std::sort(nodes.begin(), nodes.end());
    auto i = label2clique.cbegin();
    for (; i != label2clique.cend(); i++) {
        const Clique *clique = &i->second;
        if (std::includes(
            clique->nodes.begin(),
            clique->nodes.end(),
            nodes.begin(),
            nodes.end()
        )) {
            return *clique;
        }
    }
    throw std::runtime_error("No clique found with given variables.");
}

DiscreteFactor CliqueTree::get_joint_query(const Node &prev, const Node &curr, Nodes *variables) const {
    DiscreteFactor message;
    const Clique *clique = &label2clique.at(curr);

    if (clique->is_separator) {
        for (Node next : neighbors(curr)) {
            if (next != prev) {
                message *= get_joint_query(curr, next, variables);
            }
        }
        // If the returning value is not empty, this means that there
        // are variables of the query in the subtree under this separator,
        // so we need to divide the returning belief by the sepset belief. 
        message /= clique->belief;

        return message;
    }

    // Check if the current clique contains any variable of the query.
    for (Node node : clique->nodes) {
        auto variable = std::find(
            variables->begin(),
            variables->end(),
            node
        );
        if (variable != variables->end()) {
            variables->erase(variable);
        }
    }

    // If there are variables left to be found,
    // make a recursive call over children.
    for (Node next : neighbors(curr)) {
        if (next != prev && variables->size() > 0) {
            message *= get_joint_query(curr, next, variables);
        }
    }

    // If message is not empty or a variable is found,
    // then multiply the message by the clique belief.
    message *= clique->belief;
    
    return message;
}

}  // namespace algorithms

}  // namespace madbayes
