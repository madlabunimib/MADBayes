#pragma once

#include "data_array.hpp"

namespace madbayes {

namespace structures {

DataArray::DataArray() : values(1) {}

DataArray::DataArray(const Coordinates &coordinates) : coordinates(coordinates) {}

template <typename T>
DataArray::DataArray(const T &data, const Coordinates &coordinates) : coordinates(coordinates) {
    std::vector<size_t> shape;
    for (Axis axis : coordinates) shape.push_back(axis.second.size());
    values = xt::adapt(data.data(), shape);
}

DataArray::DataArray(const DataArray &other) : coordinates(other.coordinates), values(other.values) {}

DataArray &DataArray::operator=(const DataArray &other) {
    if (this != &other) {
        DataArray tmp(other);
        std::swap(tmp.coordinates, coordinates);
        std::swap(tmp.values, values);
    }
    return *this;
}

DataArray::~DataArray() {}

bool DataArray::operator==(const DataArray &other) const {
    if (coordinates != other.coordinates) return false;
    if (xt::any(xt::not_equal(values, other.values))) return false;
    return true;
}

Coordinates DataArray::get_coordinates() const { return coordinates; }

xt::xarray<double> DataArray::get_values() const { return values; }

void DataArray::set_value(const Locations locations, double value) {
    xt::xstrided_slice_vector idx;
    
    for (Axis axis : coordinates) {
        auto found = std::find_if(
            locations.begin(),
            locations.end(),
            [&](Location other) { return other.first == axis.first; }
        );
        if (found != locations.end()) {
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

    auto view = xt::strided_view(values, idx);
    view = value;
}

DataArray DataArray::adapt(const DataArray &other) const {
    DataArray out {coordinates};

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

    out.values = xt::strided_view(values, extra);

    return out;
}

DataArray &DataArray::rearrange(const DataArray &other) {
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
    values = xt::transpose(values, order);

    return *this;
}

DataArray DataArray::operator+(const DataArray &other) const {
    DataArray a, b, out;
    a = adapt(other);
    b = other.adapt(*this).rearrange(a);
    out.coordinates = a.coordinates;
    out.values = a.values + b.values;
    return out;
}

DataArray DataArray::operator-(const DataArray &other) const {
    DataArray a, b, out;
    a = adapt(other);
    b = other.adapt(*this).rearrange(a);
    out.coordinates = a.coordinates;
    out.values = a.values - b.values;
    return out;
}

DataArray DataArray::operator*(const DataArray &other) const {
    DataArray a, b, out;
    a = adapt(other);
    b = other.adapt(*this).rearrange(a);
    out.coordinates = a.coordinates;
    out.values = a.values * b.values;
    return out;
}

DataArray DataArray::operator/(const DataArray &other) const {
    DataArray a, b, out;
    a = adapt(other);
    b = other.adapt(*this).rearrange(a);
    out.coordinates = a.coordinates;
    out.values = a.values / b.values;
    // As for CPT, the case 0/0 is defined as 0
    out.values[xt::isnan(out.values)] = 0;
    return out;
}

DataArray &DataArray::operator+=(const DataArray &other) {
    DataArray a, b;
    a = adapt(other);
    b = other.adapt(*this).rearrange(a);
    coordinates = a.coordinates;
    values = a.values + b.values;
    return *this;
}

DataArray &DataArray::operator-=(const DataArray &other) {
    DataArray a, b;
    a = adapt(other);
    b = other.adapt(*this).rearrange(a);
    coordinates = a.coordinates;
    values = a.values - b.values;
    return *this;
}

DataArray &DataArray::operator*=(const DataArray &other) {
    DataArray a, b;
    a = adapt(other);
    b = other.adapt(*this).rearrange(a);
    coordinates = a.coordinates;
    values = a.values * b.values;
    return *this;
}

DataArray &DataArray::operator/=(const DataArray &other) {
    DataArray a, b;
    a = adapt(other);
    b = other.adapt(*this).rearrange(a);
    coordinates = a.coordinates;
    values = a.values / b.values;
    // As for CPT, the case 0/0 is defined as 0
    values[xt::isnan(values)] = 0;
    return *this;
}

DataArray DataArray::sum(const std::vector<std::string> &axes) const {
    DataArray out {coordinates};

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

    out.values = xt::sum(values, idx);

    return out;
}

DataArray DataArray::marginalize(const std::vector<std::string> &axes) const {
    DataArray out {coordinates};

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

    out.values = xt::sum(values, idx);

    return out;
}

DataArray DataArray::zeros_like(const DataArray &other) {
    DataArray out {other.coordinates};
    out.values = xt::zeros_like(other.values);
    return out;
}

}  // namespace structures

}  // namespace madbayes