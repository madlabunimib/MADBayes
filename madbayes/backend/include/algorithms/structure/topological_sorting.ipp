#pragma once

#include <structures/directed_graph.hpp>

namespace madbayes {

namespace structures {

Nodes topological_sorting(const DirectedGraph &other) {
    Nodes out;
    igraph_vector_t sorting;
    igraph_vector_init(&sorting, 0);
    igraph_topological_sorting(&other.graph, &sorting, IGRAPH_OUT);
    for (int i = 0; i < igraph_vector_size(&sorting); i++) {
        out.push_back(other.vid2label[VECTOR(sorting)[i]]);
    }
    igraph_vector_destroy(&sorting);
    return out;
}

}  // namespace structures

}  // namespace madbayes
