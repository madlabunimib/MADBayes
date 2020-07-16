#pragma once

#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>

#include <backend.hpp>

using namespace madbayes::structures;

namespace py = pybind11;

namespace pybind11 {
namespace detail {
template <>
struct type_caster<DataArray> {
   public:
    /**
     * This macro establishes the name 'DataArray' in
     * function signatures and declares a local variable
     * 'value' of type DataArray
     */
    PYBIND11_TYPE_CASTER(DataArray, _("DataArray"));

    /**
     * Conversion part 1 (Python->C++): convert a PyObject into a DataArray
     * instance or return false upon failure. The second argument
     * indicates whether implicit conversions should be applied.
     */
    bool load(handle src, bool) {
        // Extract object from handle
        py::object obj = reinterpret_borrow<py::object>(src).attr("to_dict")();
        // Extract members from dict
        Mapper mapper;
        py::dict coords = obj.attr("get")("coords").cast<py::dict>();
        for (auto i = coords.begin(); i != coords.end(); i++) {
            std::string dim = (i->first).cast<py::str>();
            py::dict value = (i->second).cast<py::dict>();
            std::vector<std::string> coord = (value[py::str("data")]).cast<std::vector<std::string>>();
            mapper.insert({dim, coord});
        }
        py::array_t<double> data = obj.attr("get")("data");
        // Object constructor
        value = ProbabilityTable(data, mapper);
        // Check conversion
        return !PyErr_Occurred();
    }

    /**
     * Conversion part 2 (C++ -> Python): convert an DataArray instance into
     * a Python object. The second and third arguments are used to
     * indicate the return value policy and parent object (for
     * ``return_value_policy::reference_internal``) and are generally
     * ignored by implicit casters.
     */
    static handle cast(const DataArray &src, return_value_policy /* policy */, handle /* parent */) {
        // Import modules
        py::object numpy = py::module::import("numpy");
        py::object xarray = py::module::import("xarray");

        // Get shape
        std::vector<size_t> shape;
        auto _shape = src.data().shape();
        for (auto i = _shape.begin(); i != _shape.end(); ++i) shape.push_back(*i);

        // Extract data
        std::vector<double> data;
        auto _storage = src.data().storage();
        for (auto i = _storage.begin(); i != _storage.end(); ++i) data.push_back(i->value());

        // Extract dims and coords
        std::vector<std::string> _dims;
        std::vector<std::vector<std::string>> coords;
        auto _coord = src.coordinates();
        for (auto i = _coord.begin(); i != _coord.end(); ++i) {
            std::vector<std::string> coord;
            _dims.push_back(i->first);
            size_t end = i->second.labels().size();
            auto _labels = i->second.labels().data();
            for (auto j = _labels; j < _labels + end; ++j) {
                coord.push_back(*j);
            }
            coords.push_back(coord);
        }
        // We need to freeze the dims
        py::tuple dims = py::cast(_dims);

        // Build ndarray
        py::object ndarray = numpy.attr("array")(data);
        ndarray = numpy.attr("reshape")(ndarray, shape);
        py::object out = xarray.attr("DataArray")(ndarray, coords, dims);

        return out.release();
    }
};

}  // namespace detail
}  // namespace pybind11
