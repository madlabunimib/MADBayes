#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>

#include <iostream>
#include <numeric>
#include <string>
#include <sstream>

#include <backend.hpp>
#include "pybind11_cast_xarray.ipp"

using namespace madbayes;
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
        .def(py::init<const Graph &>(), py::arg("other"))
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
        .def("is_complete", &Graph::is_complete)
        .def("is_reachable", &Graph::is_reachable, py::arg("from"), py::arg("to"))
        .def("neighbors", &Graph::neighbors, py::arg("node"))
        .def("boundary", &Graph::boundary, py::arg("nodes"))
        .def("__repr__", &Graph::__repr__)
        .def_static("random", &Graph::random, py::arg("nodes"), py::arg("edge_probability"));
    
    py::class_<DirectedGraph, Graph>(m, "DirectedGraph")
        .def(py::init<>())
        .def(py::init<const std::string &>(), py::arg("formula"))
        .def(py::init<const Nodes &>(), py::arg("nodes"))
        .def(py::init<const Edges &>(), py::arg("edges"))
        .def(py::init<const DirectedGraph &>(), py::arg("other"))
        .def("is_dag", &DirectedGraph::is_dag)
        .def("reverse_edge", &DirectedGraph::reverse_edge, py::arg("from"), py::arg("to"))
        .def("parents", &DirectedGraph::parents, py::arg("node"))
        .def("family", &DirectedGraph::family, py::arg("node"))
        .def("children", &DirectedGraph::children, py::arg("node"))
        .def("ancestors", &DirectedGraph::ancestors, py::arg("node"))
        .def("descendants", &DirectedGraph::descendants, py::arg("node"))
        .def_static("random", &DirectedGraph::random, py::arg("nodes"), py::arg("edge_probability"));
    
    m.def("ProbabilityTable", &ProbabilityTable<std::vector<double>>, py::arg("data"), py::arg("coordinates"));
    m.def("ProbabilityTable", &ProbabilityTable<py::array_t<double>>, py::arg("data"), py::arg("coordinates"));

    py::class_<BayesianNetwork, DirectedGraph>(m, "BayesianNetwork")
        .def(py::init<>())
        .def(py::init<const std::string &, const std::map<std::string, DataArray> &>(), py::arg("formula"), py::arg("cpts"))
        .def(py::init<const Nodes &, const std::map<std::string, DataArray> &>(), py::arg("nodes"), py::arg("cpts"))
        .def(py::init<const Edges &, const std::map<std::string, DataArray> &>(), py::arg("edges"), py::arg("cpts"))
        .def(py::init<const BayesianNetwork &>(), py::arg("other"))
        .def("__call__", &BayesianNetwork::operator(), py::arg("node"))
        .def("get_cpt", &BayesianNetwork::get_cpt, py::arg("node"))
        .def("set_cpt", &BayesianNetwork::set_cpt, py::arg("node"), py::arg("cpt"));

    py::class_<DiscreteBayesianNetwork, BayesianNetwork>(m, "DiscreteBayesianNetwork", py::dynamic_attr())
        .def(py::init<>())
        .def(py::init<const std::string &, const std::map<std::string, DataArray> &>(), py::arg("formula"), py::arg("cpts"))
        .def(py::init<const Nodes &, const std::map<std::string, DataArray> &>(), py::arg("nodes"), py::arg("cpts"))
        .def(py::init<const Edges &, const std::map<std::string, DataArray> &>(), py::arg("edges"), py::arg("cpts"))
        .def(py::init<const DiscreteBayesianNetwork &>(), py::arg("other"))
        .def("get_levels", &DiscreteBayesianNetwork::get_levels, py::arg("node"));
    
    // Algorithms

    // Algorithms - Inference
    py::class_<Clique>(m, "Clique")
        .def("__str__", &Clique::operator std::string)
        .def_readwrite("is_separator", &Clique::is_separator)
        .def_readwrite("nodes", &Clique::nodes)
        .def_readwrite("belief", &Clique::belief);

    py::class_<CliqueTree, Graph>(m, "CliqueTree")
        .def(py::init<const DiscreteBayesianNetwork &>(), py::arg("bn"))
        .def(py::init<const CliqueTree &>(), py::arg("other"))
        // .def("__call__", &CliqueTree::operator(), py::arg("query", py::arg("evidence")));
        .def("get_clique", &CliqueTree::get_clique, py::arg("label"))
        .def("set_clique", &CliqueTree::set_clique, py::arg("clique"));

    // Algorithms - Structure
    m.def("chain_of_cliques", &chain_of_cliques, py::arg("cliques"), py::arg("alpha"));
    m.def("chordal", &chordal, py::arg("other"));
    m.def("maximal_cliques", &maximal_cliques, py::arg("other"));
    m.def("maximum_cardinality_search", &maximum_cardinality_search, py::arg("other"));
    m.def("moral", &moral, py::arg("other"));

}