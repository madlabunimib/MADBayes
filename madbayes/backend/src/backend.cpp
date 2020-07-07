#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

#include <iostream>
#include <numeric>
#include <string>
#include <sstream>

#include <backend.hpp>

using namespace madbayes::structures;

namespace py = pybind11;

PYBIND11_MODULE(backend, m) {
    m.doc() = "MADBayes is a Python library about Bayesian Networks - Backend";
}
