#pragma once

#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>
#define FORCE_IMPORT_ARRAY
#include <xtensor-python/pyarray.hpp>

#include <backend.hpp>

using namespace madbayes;
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
            mapper.push_back({dim, coord});
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

        // Extract dims and coords
        std::vector<std::string> dims = src.dimension_labels();
        std::vector<std::vector<std::string>> coords(dims.size());
        auto coord = src.coordinates();
        for (auto i = coord.begin(); i != coord.end(); i++) {
            size_t idx = std::distance(dims.begin(), std::find(dims.begin(), dims.end(), i->first));
            size_t end = i->second.labels().size();
            auto begin = i->second.labels().data();
            for (auto j = begin; j < begin + end; j++) {
                coords[idx].push_back(*j);
            }
        }

        // Build ndarray
        py::object out = xarray.attr("DataArray")(src.data().value(), coords, dims);

        return out.release();
    }
};

}  // namespace detail
}  // namespace pybind11
