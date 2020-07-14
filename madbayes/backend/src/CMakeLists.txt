find_package(Python3 COMPONENTS Interpreter NumPy)

pybind11_add_module(backend MODULE backend.cpp)

target_link_libraries(backend PRIVATE
    pybind11::module
    Python3::NumPy
    igraph
    xsimd
    xtensor
    xtensor::optimize
    xtensor::use_xsimd
)

set_target_properties(backend PROPERTIES PREFIX "${PYTHON_MODULE_PREFIX}"
                                         SUFFIX "${PYTHON_MODULE_EXTENSION}")
