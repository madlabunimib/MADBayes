#pragma once

#include <backend.hpp>

using namespace madbayes;
using namespace madbayes::structures;

namespace py = pybind11;

namespace pybind11 {
namespace detail {
template <>
struct type_caster<DiscreteFactor> {
   public:
    /**
     * This macro establishes the name 'DiscreteFactor' in
     * function signatures and declares a local variable
     * 'value' of type DiscreteFactor
     */
    PYBIND11_TYPE_CASTER(DiscreteFactor, _("DiscreteFactor"));

    /**
     * Conversion part 1 (Python->C++): convert a PyObject into a DiscreteFactor
     * instance or return false upon failure. The second argument
     * indicates whether implicit conversions should be applied.
     */
    bool load(handle src, bool) {
        // Extract object from handle
        py::object obj = reinterpret_borrow<py::object>(src).attr("to_dict")();
        // Extract members from dict
        Coordinates axes;
        py::dict coords = obj.attr("get")("coords").cast<py::dict>();
        for (auto i = coords.begin(); i != coords.end(); i++) {
            std::string dim = (i->first).cast<py::str>();
            py::dict value = (i->second).cast<py::dict>();
            std::vector<std::string> coord = (value[py::str("data")]).cast<std::vector<std::string>>();
            axes.push_back({dim, coord});
        }
        py::array_t<double> data = obj.attr("get")("data");
        // Object constructor
        value = DiscreteFactor(data, axes);
        // Check conversion
        return !PyErr_Occurred();
    }

    /**
     * Conversion part 2 (C++ -> Python): convert an DiscreteFactor instance into
     * a Python object. The second and third arguments are used to
     * indicate the return value policy and parent object (for
     * ``return_value_policy::reference_internal``) and are generally
     * ignored by implicit casters.
     */
    static handle cast(const DiscreteFactor &src, return_value_policy /* policy */, handle /* parent */) {
        py::object xarray = py::module::import("xarray");
        py::object out = xarray.attr("DataArray")(src.get_data(), src.get_coordinates());
        return out.release();
    }
};

}  // namespace detail
}  // namespace pybind11
