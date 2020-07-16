#pragma once

#include "probability_table.hpp"

namespace madbayes {

namespace structures {

template <typename T>
DataArray ProbabilityTable(const T &data, const Mapper &coordinates) {
    std::vector<size_t> shape;
    Dimension::label_list dims;
    DataArray::coordinate_map coords;
    for (Mapper::value_type pair : coordinates) {
        dims.push_back(pair.first);
        shape.push_back(pair.second.size());
        coords[pair.first] = Axis(pair.second);
    }
    xt::xarray<double> array = xt::adapt(data.data(), shape);
    DataArray table(array, coords, dims);
    return table;
}

}  // namespace structures

}  // namespace madbayes