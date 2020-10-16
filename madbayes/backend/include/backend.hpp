#pragma once

#include "structures/discrete_factor.ipp"
#include "structures/bayesian_network.ipp"
#include "structures/discrete_bayesian_network.ipp"

#include "algorithms/inference/clique_tree.ipp"
#include "algorithms/sampling/forward_sampling.ipp"
#include "algorithms/structure/chain_cliques.ipp"

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
