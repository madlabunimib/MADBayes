#pragma once

#include <structures/graph.hpp>

namespace madbayes {

namespace structures {

Nodes maximum_cardinality_search(const Graph &other) {
    igraph_vector_t alpha;
    igraph_vector_init(&alpha, 0);
    igraph_maximum_cardinality_search(&other.graph, &alpha, 0);
    Nodes out = other.vid2label;
    for (int i = 0; i < igraph_vector_size(&alpha); i++) {
        out[VECTOR(alpha)[i]] = other.vid2label[i];
    }
    igraph_vector_destroy(&alpha);
    return out;
}

}  // namespace structures

}  // namespace madbayes
