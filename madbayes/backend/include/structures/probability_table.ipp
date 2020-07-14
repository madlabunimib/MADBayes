#pragma once

#include "probability_table.hpp"

namespace madbayes {

namespace structures {

PT ProbabilityTable(const std::vector<double> &data, const Mapper &coordinates) {
    std::vector<size_t> shape;
    PT::coordinate_map coords;
    Dimension::label_list dims;
    for (Mapper::value_type pair : coordinates) {
        dims.push_back(pair.first);
        shape.push_back(pair.second.size());
        coords[pair.first] = Axis(pair.second);
    }
    xt::xarray<double> array = xt::adapt(data, shape);
    PT table(array, coords, dims);
    return table;
}

}  // namespace structures

}  // namespace madbayes