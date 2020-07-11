#pragma once

#include <structures/directed_graph.hpp>

namespace madbayes {

namespace structures {

template<typename T>
T chordal(const T &other) {
    igraph_t chordal;
    igraph_bool_t is_chordal;
    igraph_is_chordal(&other.graph, 0, 0, &is_chordal, 0, &chordal);
    T out(&chordal);
    igraph_destroy(&chordal);
    return out;
}

}  // namespace structures

}  // namespace madbayes
