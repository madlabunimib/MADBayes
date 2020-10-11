cmake_minimum_required(VERSION 3.1)

project(MADBayes    VERSION 0.0.1
                    DESCRIPTION "MADBayes is a Python library about Bayesian Networks - Backend"
                    LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 14)

add_compile_options(-Wall -Wextra -pedantic)
add_compile_options(-O3 -march=native -shared -std=c++14 -fPIC)
add_compile_options(-Wno-unused-but-set-parameter -Wno-deprecated-copy)

add_definitions(-DXTENSOR_USE_XSIMD)

include_directories(include)

include_directories(extern/xtl/include)
add_subdirectory(extern/xtl)
set(xtl_DIR "${CMAKE_CURRENT_BINARY_DIR}/extern/xtl" CACHE STRING "" FORCE)

include_directories(extern/xsimd/include)
add_subdirectory(extern/xsimd)
set(xsimd_DIR "${CMAKE_CURRENT_BINARY_DIR}/extern/xsimd" CACHE STRING "" FORCE)

include_directories(extern/xtensor/include)
add_subdirectory(extern/xtensor)
set(xtensor_DIR "${CMAKE_CURRENT_BINARY_DIR}/extern/xtensor" CACHE STRING "" FORCE)

set(PYBIND11_CPP_STANDARD -std=c++14)
include_directories(extern/pybind11/include)
add_subdirectory(extern/pybind11)

include_directories(extern/xtensor-python/include)
add_subdirectory(extern/xtensor-python)

add_library(xtensor::use_xsimd INTERFACE IMPORTED)
target_link_libraries(xtensor::use_xsimd INTERFACE xsimd)
target_compile_definitions(xtensor::use_xsimd INTERFACE XTENSOR_USE_XSIMD)

add_library(xtensor::optimize INTERFACE IMPORTED)
target_link_libraries(xtensor::optimize INTERFACE xtensor)
target_compile_definitions(xtensor::optimize INTERFACE XTENSOR_OPTIMIZE)

add_subdirectory(src)

enable_testing()
include(GoogleTest)
add_subdirectory(tests)
