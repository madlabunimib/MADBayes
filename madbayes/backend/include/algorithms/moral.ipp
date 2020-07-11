#pragma once

#include <structures/directed_graph.hpp>

namespace madbayes {

namespace algorithms {

using Node = madbayes::structures::Node;
using Nodes = madbayes::structures::Nodes;
using Graph = madbayes::structures::Graph;
using DirectedGraph = madbayes::structures::DirectedGraph;

Graph moral(const DirectedGraph &graph) {
    Graph out = graph.to_undirected();
    for (Node node : graph.get_nodes()) {
        Nodes parents = graph.parents(node);
        for (size_t i = 0; i < parents.size(); i++)
            for (size_t j = i; j < parents.size(); j++)
                if (j != i) out.add_edge(parents[i], parents[j]);
    }
    return out;
}

}  // namespace algorithms

}  // namespace algorithms
