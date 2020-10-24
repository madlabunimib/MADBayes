#pragma once

#include "discrete_factor.hpp"

namespace madbayes {

namespace structures {

DiscreteFactor::DiscreteFactor() : data(1) {}

DiscreteFactor::DiscreteFactor(const Coordinates &coordinates) : coordinates(coordinates) {
    xt::xarray<float>::shape_type shape;
    for (Axis axis : coordinates) shape.push_back(axis.second.size());
    data = xt::zeros<float>(shape);
}

template <typename T>
DiscreteFactor::DiscreteFactor(const T &_data, const Coordinates &_coordinates) : coordinates(_coordinates) {
    std::vector<size_t> shape;
    for (Axis axis : _coordinates) shape.push_back(axis.second.size());
    data = xt::adapt(_data.data(), shape);
}

DiscreteFactor::DiscreteFactor(const DiscreteFactor &other) : data(other.data), coordinates(other.coordinates) {}

DiscreteFactor &DiscreteFactor::operator=(const DiscreteFactor &other) {
    if (this != &other) {
        DiscreteFactor tmp(other);
        std::swap(tmp.data, data);
        std::swap(tmp.coordinates, coordinates);
    }
    return *this;
}

DiscreteFactor::~DiscreteFactor() {}

bool DiscreteFactor::operator==(const DiscreteFactor &other) const {
    if (coordinates != other.coordinates) return false;
    if (xt::any(xt::not_equal(data, other.data))) return false;
    return true;
}

Coordinates DiscreteFactor::get_coordinates() const { return coordinates; }

Axis DiscreteFactor::get_axis(const std::string &axis) const {
    auto found = std::find_if(
        coordinates.begin(),
        coordinates.end(),
        [&](const Axis &other) { return other.first == axis; }
    );
    
    if (found == coordinates.end()) {
        throw std::runtime_error("No axis found with given name.");
    }

    return *found;
}

Level DiscreteFactor::get_level(const std::string &axis, size_t idx) const {
    return get_axis(axis).second[idx];
}

Levels DiscreteFactor::get_levels(const std::string &axis) const {
    return get_axis(axis).second;
}

xt::xarray<float> DiscreteFactor::get_data() const { return data; }

auto DiscreteFactor::get_slice(const Evidence &evidence) {
    xt::xstrided_slice_vector idx;
    
    for (Axis axis : coordinates) {
        auto found = std::find_if(
            evidence.begin(),
            evidence.end(),
            [&](Evidence::value_type other) { return other.first == axis.first; }
        );
        if (found != evidence.end()) {
            auto id = std::find(
                axis.second.begin(),
                axis.second.end(),
                found->second
            );
            if (id != axis.second.end()) {
                idx.push_back(std::distance(axis.second.begin(), id));
            }
        } else {
            idx.push_back(xt::all());
        }
    }

    return xt::strided_view(data, idx);
}

void DiscreteFactor::set_value(const Evidence &evidence, double value) {
    auto view = get_slice(evidence);
    view = value;
}

bool DiscreteFactor::empty() const {
    return coordinates.empty();
}

DiscreteFactor DiscreteFactor::adapt(const DiscreteFactor &other) const {
    DiscreteFactor out {coordinates};

    // Add extra dims
    xt::xstrided_slice_vector extra { xt::ellipsis() };

    for (Axis axis : other.coordinates) {
        auto found = std::find(
            out.coordinates.begin(),
            out.coordinates.end(),
            axis
        );
        if (found == out.coordinates.end()) {
            out.coordinates.push_back(axis);
            extra.push_back(xt::newaxis());
        }
    }

    out.data = xt::strided_view(data, extra);

    return out;
}

DiscreteFactor &DiscreteFactor::rearrange(const DiscreteFactor &other) {
    // Compute dims order
    std::vector<size_t> order;
    for (size_t i = 0; i < other.coordinates.size(); i++) {
        auto found = std::find(
            coordinates.cbegin(),
            coordinates.cend(),
            other.coordinates[i]
        );
        order.push_back(i);
        if (found != coordinates.cend()) {
            order[i] = std::distance(coordinates.cbegin(), found);
        }
    }

    // Rearrange data using transpose
    data = xt::transpose(data, order);

    return *this;
}

DiscreteFactor DiscreteFactor::operator+(const DiscreteFactor &other) const {
    if (other.empty()) return *this;

    DiscreteFactor a, b, out;
    a = adapt(other);
    b = other.adapt(*this).rearrange(a);
    out.coordinates = a.coordinates;
    out.data = a.data + b.data;
    return out;
}

DiscreteFactor DiscreteFactor::operator-(const DiscreteFactor &other) const {
    if (other.empty()) return *this;

    DiscreteFactor a, b, out;
    a = adapt(other);
    b = other.adapt(*this).rearrange(a);
    out.coordinates = a.coordinates;
    out.data = a.data - b.data;
    return out;
}

DiscreteFactor DiscreteFactor::operator*(const DiscreteFactor &other) const {
    if (other.empty()) return *this;

    DiscreteFactor a, b, out;
    a = adapt(other);
    b = other.adapt(*this).rearrange(a);
    out.coordinates = a.coordinates;
    out.data = a.data * b.data;
    return out;
}

DiscreteFactor DiscreteFactor::operator/(const DiscreteFactor &other) const {
    if (other.empty()) return *this;

    DiscreteFactor a, b, out;
    a = adapt(other);
    b = other.adapt(*this).rearrange(a);
    out.coordinates = a.coordinates;
    out.data = a.data / b.data;
    // As for DiscreteFactor, the case 0/0 is defined as 0
    out.data = xt::nan_to_num(out.data);
    return out;
}

DiscreteFactor &DiscreteFactor::operator+=(const DiscreteFactor &other) {
    if (other.empty()) return *this;

    DiscreteFactor a, b, out;
    a = adapt(other);
    b = other.adapt(*this).rearrange(a);
    coordinates = a.coordinates;
    data = a.data + b.data;
    return *this;
}

DiscreteFactor &DiscreteFactor::operator-=(const DiscreteFactor &other) {
    if (other.empty()) return *this;

    DiscreteFactor a, b, out;
    a = adapt(other);
    b = other.adapt(*this).rearrange(a);
    coordinates = a.coordinates;
    data = a.data - b.data;
    return *this;
}

DiscreteFactor &DiscreteFactor::operator*=(const DiscreteFactor &other) {
    if (other.empty()) return *this;

    DiscreteFactor a, b, out;
    a = adapt(other);
    b = other.adapt(*this).rearrange(a);
    coordinates = a.coordinates;
    data = a.data * b.data;
    return *this;
}

DiscreteFactor &DiscreteFactor::operator/=(const DiscreteFactor &other) {
    if (other.empty()) return *this;

    DiscreteFactor a, b, out;
    a = adapt(other);
    b = other.adapt(*this).rearrange(a);
    coordinates = a.coordinates;
    data = a.data / b.data;
    // As for DiscreteFactor, the case 0/0 is defined as 0
    data = xt::nan_to_num(data);
    return *this;
}

DiscreteFactor DiscreteFactor::sum(const std::vector<std::string> &axes) const {
    DiscreteFactor out {coordinates};

    std::vector<size_t> idx;
    auto i = out.coordinates.begin();
    for (; i != out.coordinates.end(); i++) {
        auto found = std::find_if(
            axes.begin(),
            axes.end(),
            [&](std::string other) { return other == i->first; }
        );
        if (found != axes.end()) {
            size_t offset = std::distance(out.coordinates.begin(), i);
            idx.push_back(idx.size() + offset);
            out.coordinates.erase(i--);
        }
    }

    out.data = xt::sum(data, idx);

    return out;
}

DiscreteFactor DiscreteFactor::marginalize(const std::vector<std::string> &axes) const {
    DiscreteFactor out {coordinates};

    std::vector<size_t> idx;
    auto i = out.coordinates.begin();
    for (; i != out.coordinates.end(); i++) {
        auto found = std::find_if(
            axes.begin(),
            axes.end(),
            [&](std::string other) { return other == i->first; }
        );
        if (found == axes.end()) {
            size_t offset = std::distance(out.coordinates.begin(), i);
            idx.push_back(idx.size() + offset);
            out.coordinates.erase(i--);
        }
    }

    out.data = xt::sum(data, idx);

    return out;
}

DiscreteFactor DiscreteFactor::normalize() const {
    DiscreteFactor out(*this);
    xt::xarray<float> sum = xt::sum(data);
    out.data /= sum;
    return out;
}

DiscreteFactor DiscreteFactor::zeros_like(const DiscreteFactor &other) {
    DiscreteFactor out {other.coordinates};
    out.data = xt::zeros_like(other.data);
    return out;
}

}  // namespace structures

}  // namespace madbayes