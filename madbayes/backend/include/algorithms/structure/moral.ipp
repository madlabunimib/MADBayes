#pragma once

#include <structures/directed_graph.hpp>

namespace madbayes {

namespace algorithms {

using Graph = madbayes::structures::Graph;
using DirectedGraph = madbayes::structures::DirectedGraph;

Graph moral(const DirectedGraph &other) {
    Graph out = other.to_undirected();
    for (Node node : other.get_nodes()) {
        Nodes parents = other.parents(node);
        for (size_t i = 0; i < parents.size(); i++)
            for (size_t j = i; j < parents.size(); j++)
                if (j != i) out.add_edge(parents[i], parents[j]);
    }
    return out;
}

}  // namespace algorithms

}  // namespace madbayes
