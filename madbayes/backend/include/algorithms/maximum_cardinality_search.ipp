#pragma once

#include <structures/graph.hpp>

namespace madbayes {

namespace structures {

std::vector<size_t> maximum_cardinality_search(const Graph &other) {
    igraph_vector_t alpha;
    igraph_maximum_cardinality_search(&other.graph, &alpha, 0);
    std::vector<size_t> out;
    for (int i = 0; i < igraph_vector_size(&alpha); i++) {
        out.push_back(VECTOR(alpha)[i]);
    }
    return out;
}

}  // namespace structures

}  // namespace madbayes
