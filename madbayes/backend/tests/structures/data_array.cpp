#include <gtest/gtest.h>

#include "structures/data_array.ipp"

using namespace madbayes;
using namespace madbayes::structures;

TEST(TestDataArray, AddOperator) {}

TEST(TestDataArray, SubOperator) {}

TEST(TestDataArray, MulOperator) {
    DataArray a {
        std::vector<double>({0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11}),
        {{"x1", {"1", "2"}}, {"x2", {"1", "2", "3"}}, {"x3", {"1", "2"}}}
    };
    DataArray b {
        std::vector<double>({0, 1, 2, 3, 4, 5, 6, 7, 8}),
        {{"x3", {"1", "2"}}, {"x4", {"1", "2"}}, {"x1", {"1", "2"}}}
    };
    DataArray c = {
        std::vector<double>({0, 0, 4, 6, 0, 4, 12, 18, 0, 8, 20, 30, 6, 18, 35, 49, 8, 24, 45, 63, 10, 30, 55, 77}),
        {{"x1", {"1", "2"}}, {"x2", {"1", "2", "3"}}, {"x3", {"1", "2"}}, {"x4", {"1", "2"}}}
    };
    ASSERT_EQ(c.get_coordinates(), (a * b).get_coordinates());
    ASSERT_EQ(c.get_values(), (a * b).get_values());
}

TEST(TestDataArray, DivOperator) {
    DataArray a {
        std::vector<double>({0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11}),
        {{"x1", {"1", "2"}}, {"x2", {"1", "2", "3"}}, {"x3", {"1", "2"}}}
    };
    DataArray b {
        std::vector<double>({1, 2, 3, 4}),
        {{"x3", {"1", "2"}}, {"x1", {"1", "2"}}}
    };
    DataArray c = {
        std::vector<double>({0, 1.0/3.0, 2, 1, 4, 5.0/3.0, 3, 1.75, 4, 2.25, 5, 2.75}),
        {{"x1", {"1", "2"}}, {"x2", {"1", "2", "3"}}, {"x3", {"1", "2"}}}
    };
    ASSERT_EQ(c.get_coordinates(), (a / b).get_coordinates());
    ASSERT_EQ(c.get_values(), (a / b).get_values());
}
