#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>

#include <iostream>
#include <numeric>
#include <string>
#include <sstream>

#include <backend.hpp>

using namespace madbayes::structures;

namespace py = pybind11;

PYBIND11_MODULE(backend, m) {
    m.doc() = "MADBayes is a Python library about Bayesian Networks - Backend";

    py::class_<Graph>(m, "Graph")
        .def(py::init<const std::string &>())
        .def(py::init<const Nodes &>())
        .def(py::init<const Edges &>())
        .def_property("nodes", &Graph::get_nodes, &Graph::set_nodes)
        .def_property_readonly("edges", &Graph::get_edges)
        .def("add_node", &Graph::add_node)
        .def("remove_node", &Graph::remove_node)
        .def("add_edge", &Graph::add_edge)
        .def("remove_edge", &Graph::remove_edge)
        .def("subgraph", &Graph::subgraph)
        .def("is_directed", &Graph::is_directed)
        .def("is_chordal", &Graph::is_chordal)
        .def("neighbors", &Graph::neighbors)
        .def("boundary", &Graph::boundary);
}
