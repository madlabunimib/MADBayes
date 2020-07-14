#include <gtest/gtest.h>

#include "structures/probability_table.ipp"

using namespace madbayes::structures;

TEST(TestProbabilityTable, ProbabilityTable) {
    std::vector<double> data = {1.0, 2.0, 3.0, 4.0};
    Mapper mapper = {{"A", {"0", "1"}}, {"B", {"2", "3"}}};
    PT table = ProbabilityTable(data, mapper);
    double selected = table.locate("1", "2").value();
    ASSERT_FLOAT_EQ(selected, 3.0);
}
