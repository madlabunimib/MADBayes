#pragma once

#include <map>
#include <string>
#include <vector>
#include <xframe/xio.hpp>
#include <xframe/xvariable.hpp>
#include <xtensor/xadapt.hpp>
#include <xtensor/xarray.hpp>

namespace madbayes {

namespace structures {

using Axis = xf::xaxis<std::string>;
using Coordinate = xf::xcoordinate<std::string, xtl::mpl::vector<std::string>>;
using Dimension = xf::xdimension<std::string>;
using PT = xf::xvariable<double, Coordinate>;

using Mapper = std::map<std::string, std::vector<std::string>>;

PT ProbabilityTable(const std::vector<double> &data, const Mapper &coordinates);

}  // namespace structures

}  // namespace madbayes