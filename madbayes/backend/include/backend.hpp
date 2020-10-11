#pragma once

#include "structures/graph.ipp"
#include "structures/directed_graph.ipp"
#include "structures/data_array.ipp"
#include "structures/bayesian_network.ipp"
#include "structures/discrete_bayesian_network.ipp"

#include "algorithms/inference/clique_tree.ipp"
#include "algorithms/structure/chain_cliques.ipp"
#include "algorithms/structure/chordal.ipp"
#include "algorithms/structure/maximal_cliques.ipp"
#include "algorithms/structure/maximum_cardinality_search.ipp"
#include "algorithms/structure/moral.ipp"
#include "algorithms/structure/topological_sorting.ipp"

#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>

#include <iostream>
#include <numeric>
#include <string>
#include <sstream>

#define FORCE_IMPORT_ARRAY
#include <xtensor-python/pyarray.hpp>
