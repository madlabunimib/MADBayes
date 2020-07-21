#pragma once

#include <structures/graph.hpp>

namespace madbayes {

namespace structures {

std::vector<Nodes> maximal_cliques(const Graph &other) {
    std::vector<Nodes> out;
    igraph_vector_ptr_t cliques;
    igraph_vector_ptr_init(&cliques, 0);
    igraph_maximal_cliques(&other.graph, &cliques, 0, 0);
    for (int i = 0; i < igraph_vector_ptr_size(&cliques); i++) {
        Nodes clique;
        igraph_vector_t *vector = (igraph_vector_t *) VECTOR(cliques)[i];
        for (int j = 0; j < igraph_vector_size(vector); j++) {
            clique.push_back(other.vid2label[(vector)->stor_begin[j]]);
        }
        out.push_back(clique);
    }
    igraph_vector_ptr_destroy_all(&cliques);
    return out;
}

}  // namespace structures

}  // namespace madbayes
