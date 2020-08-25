#pragma once

#include <map>
#include <string>
#include <vector>
#include <xframe/xio.hpp>
#include <xframe/xvariable.hpp>
#include <xframe/xvariable_view.hpp>
#include <xtensor/xadapt.hpp>
#include <xtensor/xarray.hpp>
#include <xtensor/xmath.hpp>

namespace madbayes {

using Axis = xf::xaxis<std::string>;
using Coordinate = xf::xcoordinate<std::string, xtl::mpl::vector<std::string>>;
using Dimension = xf::xdimension<std::string>;
using DataArray = xf::xvariable<double, Coordinate>;

namespace structures {

using Mapper = std::map<std::string, std::vector<std::string>>;

template <typename T>
DataArray ProbabilityTable(const T &data, const Mapper &coordinates);

}  // namespace structures

}  // namespace madbayes