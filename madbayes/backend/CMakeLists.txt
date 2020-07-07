cmake_minimum_required(VERSION 3.1)

project(MADBayes    VERSION 0.0.1
                    DESCRIPTION "MADBayes is a Python library about Bayesian Networks - Backend"
                    LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 14)

add_compile_options(-Wall -Wextra -pedantic)
add_compile_options(-O3 -march=native -shared -std=c++14 -fPIC)

include_directories(include)

set(PYBIND11_CPP_STANDARD -std=c++14)
include_directories(extern/pybind11/include)
add_subdirectory(extern/pybind11)

add_subdirectory(src)

enable_testing()
include(GoogleTest)
add_subdirectory(tests)
