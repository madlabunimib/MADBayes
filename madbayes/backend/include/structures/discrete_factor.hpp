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

using Evidence = std::map<std::string, std::string>;
using Axis = std::pair<std::string, std::vector<std::string>>;
using Coordinates = std::vector<Axis>;

namespace structures {

class DiscreteFactor {
   private:
    xt::xarray<double> data;
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
    xt::xarray<double> get_data() const;
    xt::xarray<double> get_slice(const Evidence &evidence) const;
    void set_value(const Evidence &evidence, double value);

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

    static DiscreteFactor zeros_like(const DiscreteFactor &other);
};

}  // namespace structures

}  // namespace madbayes