#pragma once

#include <map>
#include <string>
#include <vector>
#include <xtensor/xadapt.hpp>
#include <xtensor/xarray.hpp>
#include <xtensor/xio.hpp>
#include <xtensor/xmath.hpp>
#include <xtensor/xstrided_view.hpp>

namespace madbayes {

using Level = std::string;
using Levels = std::vector<Level>;
using Evidence = std::map<std::string, Level>;
using Axis = std::pair<std::string, Levels>;
using Coordinates = std::vector<Axis>;

namespace structures {

class DiscreteFactor {
   private:
    xt::xarray<float> data;
    Coordinates coordinates;

    DiscreteFactor adapt(const DiscreteFactor &other) const;
    DiscreteFactor &rearrange(const DiscreteFactor &other);

   public:
    DiscreteFactor();
    explicit DiscreteFactor(const Coordinates &coordinates);

    template <typename T>
    DiscreteFactor(const T &data, const Coordinates &coordinates);
    DiscreteFactor(const DiscreteFactor &other);
    DiscreteFactor &operator=(const DiscreteFactor &other);
    ~DiscreteFactor();

    bool operator==(const DiscreteFactor &other) const;

    Coordinates get_coordinates() const;
    Axis get_axis(const std::string &axis) const;
    Level get_level(const std::string &axis, size_t idx) const;
    Levels get_levels(const std::string &axis) const;

    xt::xarray<float> get_data() const;
    auto get_slice(const Evidence &evidence);
    void set_value(const Evidence &evidence, double value);

    bool empty() const;

    DiscreteFactor operator+(const DiscreteFactor &other) const;
    DiscreteFactor operator-(const DiscreteFactor &other) const;
    DiscreteFactor operator*(const DiscreteFactor &other) const;
    DiscreteFactor operator/(const DiscreteFactor &other) const;

    DiscreteFactor &operator+=(const DiscreteFactor &other);
    DiscreteFactor &operator-=(const DiscreteFactor &other);
    DiscreteFactor &operator*=(const DiscreteFactor &other);
    DiscreteFactor &operator/=(const DiscreteFactor &other);

    DiscreteFactor sum(const std::vector<std::string> &axes) const;
    DiscreteFactor marginalize(const std::vector<std::string> &axes) const;
    DiscreteFactor normalize() const;

    static DiscreteFactor zeros_like(const DiscreteFactor &other);
};

}  // namespace structures

}  // namespace madbayes