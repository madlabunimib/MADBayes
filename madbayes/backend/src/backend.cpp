#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>

#include <iostream>
#include <numeric>
#include <string>
#include <sstream>

#include <backend.hpp>

using namespace madbayes::algorithms;
using namespace madbayes::structures;

namespace py = pybind11;

PYBIND11_MODULE(backend, m) {
    m.doc() = "MADBayes is a Python library about Bayesian Networks - Backend";

    // Stuctures

    py::class_<Graph>(m, "Graph")
        .def(py::init<>())
        .def(py::init<const std::string &>(), py::arg("formula"))
        .def(py::init<const Nodes &>(), py::arg("nodes"))
        .def(py::init<const Edges &>(), py::arg("edges"))
        .def_property("nodes", &Graph::get_nodes, &Graph::set_nodes)
        .def_property_readonly("edges", &Graph::get_edges)
        .def("has_node", &Graph::has_node, py::arg("node"))
        .def("add_node", &Graph::add_node, py::arg("node"))
        .def("remove_node", &Graph::remove_node, py::arg("node"))
        .def("has_edge", &Graph::has_edge, py::arg("from"), py::arg("to"))
        .def("add_edge", &Graph::add_edge, py::arg("from"), py::arg("to"))
        .def("remove_edge", &Graph::remove_edge, py::arg("from"), py::arg("to"))
        .def("subgraph", &Graph::subgraph, py::arg("nodes"))
        .def("is_directed", &Graph::is_directed)
        .def("is_chordal", &Graph::is_chordal)
        .def("neighbors", &Graph::neighbors, py::arg("node"))
        .def("boundary", &Graph::boundary, py::arg("nodes"))
        .def("__repr__", &Graph::__repr__)
        .def_static("random", &Graph::random, py::arg("nodes"), py::arg("edge_probability"));
    
    py::class_<DirectedGraph, Graph>(m, "DirectedGraph")
        .def(py::init<>())
        .def(py::init<const std::string &>(), py::arg("formula"))
        .def(py::init<const Nodes &>(), py::arg("nodes"))
        .def(py::init<const Edges &>(), py::arg("edges"))
        .def("is_dag", &DirectedGraph::is_dag)
        .def("parents", &DirectedGraph::parents, py::arg("node"))
        .def("family", &DirectedGraph::family, py::arg("node"))
        .def("children", &DirectedGraph::children, py::arg("node"))
        .def("ancestors", &DirectedGraph::ancestors, py::arg("node"))
        .def("descendants", &DirectedGraph::descendants, py::arg("node"))
        .def_static("random", &DirectedGraph::random, py::arg("nodes"), py::arg("edge_probability"));
    
    // Algorithms

    m.def("chordal", &chordal<Graph>, py::arg("other"));
    m.def("chordal", &chordal<DirectedGraph>, py::arg("other"));
    m.def("maximal_cliques", &maximal_cliques, py::arg("other"));
    m.def("moral", &moral, py::arg("other"));

}
