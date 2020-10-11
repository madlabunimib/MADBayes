#include <gtest/gtest.h>

#include "algorithms/inference/clique_tree.ipp"
#include "structures/discrete_bayesian_network.ipp"

using namespace madbayes;
using namespace madbayes::algorithms;
using namespace madbayes::structures;

TEST(TestCliqueTree, DefaultContructor) {
    CPTs cpts;
    std::vector<double> vA = {0.1, 0.9};
    Coordinates mA = {{"A", {"1", "2"}}};
    cpts.insert({"A", DiscreteFactor(vA, mA)});
    std::vector<double> vB = {0.1, 0.9, 0.5, 0.5};
    Coordinates mB = {{"A", {"1", "2"}}, {"B", {"3", "4"}}};
    cpts.insert({"B", DiscreteFactor(vB, mB)});
    DiscreteBayesianNetwork bn("[A][B|A]", cpts);
    // CliqueTree jt(bn);
}
