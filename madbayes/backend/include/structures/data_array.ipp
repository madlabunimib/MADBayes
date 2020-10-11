#pragma once

#include "data_array.hpp"

namespace madbayes {

namespace structures {

DataArray::DataArray() : data(1) {}

DataArray::DataArray(const Coordinates &coordinates) : data(1), coordinates(coordinates) {}

template <typename T>
DataArray::DataArray(const T &_data, const Coordinates &_coordinates) : coordinates(_coordinates) {
    std::vector<size_t> shape;
    for (Axis axis : _coordinates) shape.push_back(axis.second.size());
    data = xt::adapt(_data.data(), shape);
}

DataArray::DataArray(const DataArray &other) : data(other.data), coordinates(other.coordinates) {}

DataArray &DataArray::operator=(const DataArray &other) {
    if (this != &other) {
        DataArray tmp(other);
        std::swap(tmp.data, data);
        std::swap(tmp.coordinates, coordinates);
    }
    return *this;
}

DataArray::~DataArray() {}

bool DataArray::operator==(const DataArray &other) const {
    if (coordinates != other.coordinates) return false;
    if (xt::any(xt::not_equal(data, other.data))) return false;
    return true;
}

Coordinates DataArray::get_coordinates() const { return coordinates; }

xt::xarray<double> DataArray::get_data() const { return data; }

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

    auto view = xt::strided_view(data, idx);
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

    out.data = xt::strided_view(data, extra);

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
    data = xt::transpose(data, order);

    return *this;
}

DataArray DataArray::operator+(const DataArray &other) const {
    DataArray a, b, out;
    a = adapt(other);
    b = other.adapt(*this).rearrange(a);
    out.coordinates = a.coordinates;
    out.data = a.data + b.data;
    return out;
}

DataArray DataArray::operator-(const DataArray &other) const {
    DataArray a, b, out;
    a = adapt(other);
    b = other.adapt(*this).rearrange(a);
    out.coordinates = a.coordinates;
    out.data = a.data - b.data;
    return out;
}

DataArray DataArray::operator*(const DataArray &other) const {
    DataArray a, b, out;
    a = adapt(other);
    b = other.adapt(*this).rearrange(a);
    out.coordinates = a.coordinates;
    out.data = a.data * b.data;
    return out;
}

DataArray DataArray::operator/(const DataArray &other) const {
    DataArray a, b, out;
    a = adapt(other);
    b = other.adapt(*this).rearrange(a);
    out.coordinates = a.coordinates;
    out.data = a.data / b.data;
    // As for CPT, the case 0/0 is defined as 0
    out.data = xt::nan_to_num(out.data);
    return out;
}

DataArray &DataArray::operator+=(const DataArray &other) {
    DataArray a, b, out;
    a = adapt(other);
    b = other.adapt(*this).rearrange(a);
    coordinates = a.coordinates;
    data = a.data + b.data;
    return *this;
}

DataArray &DataArray::operator-=(const DataArray &other) {
    DataArray a, b, out;
    a = adapt(other);
    b = other.adapt(*this).rearrange(a);
    coordinates = a.coordinates;
    data = a.data - b.data;
    return *this;
}

DataArray &DataArray::operator*=(const DataArray &other) {
    DataArray a, b, out;
    a = adapt(other);
    b = other.adapt(*this).rearrange(a);
    coordinates = a.coordinates;
    data = a.data * b.data;
    return *this;
}

DataArray &DataArray::operator/=(const DataArray &other) {
    DataArray a, b, out;
    a = adapt(other);
    b = other.adapt(*this).rearrange(a);
    coordinates = a.coordinates;
    data = a.data / b.data;
    // As for CPT, the case 0/0 is defined as 0
    data = xt::nan_to_num(data);
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

    out.data = xt::sum(data, idx);

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

    out.data = xt::sum(data, idx);

    return out;
}

DataArray DataArray::zeros_like(const DataArray &other) {
    DataArray out {other.coordinates};
    out.data = xt::zeros_like(other.data);
    return out;
}

}  // namespace structures

}  // namespace madbayes