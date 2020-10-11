#pragma once

#include <map>
#include <string>
#include <vector>
#include <xtensor/xadapt.hpp>
#include <xtensor/xarray.hpp>
#include <xtensor/xmath.hpp>
#include <xtensor/xio.hpp>
#include <xtensor/xstrided_view.hpp>

namespace madbayes {

using Axis = std::pair<std::string, std::vector<std::string>>;
using Coordinates = std::vector<Axis>;
using Location = std::pair<std::string, std::string>;
using Locations = std::vector<Location>;

namespace structures {

class DataArray {
   private:
    xt::xarray<double> data;
    Coordinates coordinates;

    DataArray adapt(const DataArray &other) const;
    DataArray &rearrange(const DataArray &other);

   public:
    DataArray();
    explicit DataArray(const Coordinates &coordinates);
    // explicit DataArray(const xt::xarray<double> &data, const Coordinates &coordinates);

    template <typename T>
    DataArray(const T &data, const Coordinates &coordinates);
    DataArray(const DataArray &other);
    DataArray &operator=(const DataArray &other);
    ~DataArray();

    bool operator==(const DataArray &other) const;

    Coordinates get_coordinates() const;
    xt::xarray<double> get_data() const;
    void set_value(const Locations locations, double value);

    DataArray operator+(const DataArray &other) const;
    DataArray operator-(const DataArray &other) const;
    DataArray operator*(const DataArray &other) const;
    DataArray operator/(const DataArray &other) const;

    DataArray &operator+=(const DataArray &other);
    DataArray &operator-=(const DataArray &other);
    DataArray &operator*=(const DataArray &other);
    DataArray &operator/=(const DataArray &other);

    DataArray sum(const std::vector<std::string> &axes) const;
    DataArray marginalize(const std::vector<std::string> &axes) const;

    static DataArray zeros_like(const DataArray &other);
};

}  // namespace structures

}  // namespace madbayes