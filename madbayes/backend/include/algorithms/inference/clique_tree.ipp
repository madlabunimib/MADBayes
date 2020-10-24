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
        if (label2clique.find(*k) == label2clique.end()) {
            add_node(*k);
            set_clique(*k);
        }
        // Add separator
        Clique separator {true, sepset, {}};
        if (label2clique.find(separator) == label2clique.end()) {
            add_node(separator);
            set_clique(separator);
        }
        add_edge(*k, separator);
        // Add Ci
        if (label2clique.find(*i) == label2clique.end()) {
            add_node(*i);
            set_clique(*i);
        }
        add_edge(separator, *i);
    }
}

DiscreteFactor CliqueTree::calibrate_upward(const Node &prev, const Node &curr) {
    DiscreteFactor message;
    for (const Node &next : neighbors(curr)) {
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

    for (const Node &next : neighbors(curr)) {
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

CliqueTree::CliqueTree(const CliqueTree &other) : Graph(other), label2clique(other.label2clique), node2clique(other.node2clique) {}

CliqueTree &CliqueTree::operator=(const CliqueTree &other) {
    if (this != &other) {
        CliqueTree tmp(other);
        std::swap(tmp.graph, graph);
        std::swap(tmp.labels, labels);
        std::swap(tmp.index, index);
        std::swap(tmp.label2clique, label2clique);
        std::swap(tmp.node2clique, node2clique);
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
        for (const Node &variable : variables) {
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
            Node root = *node2clique.at(variables[0]).begin();
            Nodes scope = Nodes(variables.begin(), variables.end());
            joint = copy.get_joint_query("", root, &scope);
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
    if (!clique.is_separator) {
        for (const Node &node : clique.nodes) {
            node2clique[node].insert(clique);
        }
    }
}

Clique CliqueTree::get_clique_given_variables(const Nodes &variables) const {
    std::set<Node> found, intersection;
    auto i = variables.begin();
    found = node2clique.at(*i++);
    for (; i != variables.end(); i++) {
        Node pointer = *i;
        std::set_intersection(
            found.begin(),
            found.end(),
            node2clique.at(pointer).begin(),
            node2clique.at(pointer).end(),
            std::inserter(intersection, intersection.end())
        );
        found = intersection;
        intersection.clear();
        if (found.empty()) {
            throw std::runtime_error("No clique found with given variables.");
        }
    }

    std::map<size_t, Node> order;
    for (const Node &node : found) {
        order.insert({label2clique.at(node).nodes.size(), node});
    }

    return label2clique.at(order.begin()->second);
}

DiscreteFactor CliqueTree::get_joint_query(const Node &prev, const Node &curr, Nodes *variables) const {
    DiscreteFactor message;
    const Clique *clique = &label2clique.at(curr);

    if (clique->is_separator) {
        for (const Node &next : neighbors(curr)) {
            if (next != prev) {
                message *= get_joint_query(curr, next, variables);
            }
        }
        // If the returning value is not empty, this means that there
        // are variables of the query in the subtree under this separator,
        // so we need to divide the returning belief by the sepset belief. 
        if (!message.empty()) {
            message /= clique->belief;
        }

        return message;
    }

    // Check if the current clique contains any variable of the query.
    bool found = false;
    for (const Node &node : clique->nodes) {
        auto variable = std::find(
            variables->begin(),
            variables->end(),
            node
        );
        if (variable != variables->end()) {
            variables->erase(variable);
            found = true;
        }
    }

    // If there are variables left to be found,
    // make a recursive call over children.
    for (const Node &next : neighbors(curr)) {
        if (next != prev && variables->size() > 0) {
            message *= get_joint_query(curr, next, variables);
        }
    }

    // If message is not empty or a variable is found,
    // then multiply the message by the clique belief.
    if (found || !message.empty()) {
        message *= clique->belief;
    }
    
    return message;
}

}  // namespace algorithms

}  // namespace madbayes
