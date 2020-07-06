#include <gtest/gtest.h>

#include "structures/directed_graph.ipp"

#define N 10

using namespace madbayes::structures;

TEST(TestDirectedGraph, DefaultContructor) {
    DirectedGraph g(N);
    ASSERT_EQ(g.size(), N);
}

TEST(TestDirectedGraph, CopyConstructor) {
    DirectedGraph g0(N);
    DirectedGraph g1(g0);
    ASSERT_EQ(g0.size(), g1.size());
}

TEST(TestDirectedGraph, AssignmentConstructor) {
    DirectedGraph g0(N);
    DirectedGraph g1 = g0;
    ASSERT_EQ(g0.size(), g1.size());
}

TEST(TestDirectedGraph, Destructor) {
    DirectedGraph *g = new DirectedGraph(N);
    ASSERT_EQ(g->size(), N);
    delete g;
}

TEST(TestDirectedGraph, Size) {
    DirectedGraph g(N);
    ASSERT_EQ(g.size(), N);
}

TEST(TestDirectedGraph, IsDirected) {
    DirectedGraph g(N);
    ASSERT_TRUE(g.is_directed());
}
