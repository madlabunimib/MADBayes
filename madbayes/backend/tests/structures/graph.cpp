#include <gtest/gtest.h>

#include "structures/graph.ipp"

#define N 10

using namespace madbayes::structures;

TEST(TestGraph, DefaultContructor) {
    Graph g(N);
    ASSERT_EQ(g.size(), N);
}

TEST(TestGraph, CopyConstructor) {
    Graph g0(N);
    Graph g1(g0);
    ASSERT_EQ(g0.size(), g1.size());
}

TEST(TestGraph, AssignmentConstructor) {
    Graph g0(N);
    Graph g1 = g0;
    ASSERT_EQ(g0.size(), g1.size());
}

TEST(TestGraph, Destructor) {
    Graph *g = new Graph(N);
    ASSERT_EQ(g->size(), N);
    delete g;
}
