#pragma once

#include <map>
#include <string>
#include <vector>
#include <xtensor/xadapt.hpp>
#include <xtensor/xarray.hpp>
#include <xtensor/xmath.hpp>
#include <xtensor/xstrided_view.hpp>

namespace madbayes {

using Axis = std::pair<std::string, std::vector<std::string>>;
using Coordinates = std::vector<Axis>;

namespace structures {

class DataArray {
   private:
    Coordinates coordinates;
    xt::xarray<double> values;

    DataArray adapt(const DataArray &other) const;
    DataArray &rearrange(const DataArray &other);

   public:
    DataArray();
    explicit DataArray(const Coordinates &coordinates);
    explicit DataArray(const xt::xarray<double> &data, const Coordinates &coordinates);

    template <typename T>
    DataArray(const T &data, const Coordinates &coordinates);
    DataArray(const DataArray &other);
    DataArray &operator=(const DataArray &other);
    ~DataArray();

    bool operator==(const DataArray &other) const;

    Coordinates get_coordinates() const;
    xt::xarray<double> get_values() const;

    DataArray operator+(const DataArray &other) const;
    DataArray operator-(const DataArray &other) const;
    DataArray operator*(const DataArray &other) const;
    DataArray operator/(const DataArray &other) const;

    DataArray &operator+=(const DataArray &other);
    DataArray &operator-=(const DataArray &other);
    DataArray &operator*=(const DataArray &other);
    DataArray &operator/=(const DataArray &other);

    DataArray sum(const std::vector<std::string> axes) const;
};

}  // namespace structures

}  // namespace madbayes