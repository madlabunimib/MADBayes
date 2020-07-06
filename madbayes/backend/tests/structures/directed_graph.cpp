#include <gtest/gtest.h>

#include "structures/directed_graph.ipp"

#define N {"1", "2", "3", "4", "5"}
#define N_SIZE 5

using namespace madbayes::structures;

TEST(TestDirectedGraph, DefaultContructor) {
    DirectedGraph g(N);
    ASSERT_EQ(g.size(), N_SIZE);
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
    ASSERT_EQ(g->size(), N_SIZE);
    delete g;
}

TEST(TestDirectedGraph, PointerContructor) {
    igraph_t ig;
    igraph_empty(&ig, N_SIZE, IGRAPH_DIRECTED);
    DirectedGraph g(&ig);
    ASSERT_EQ(g.size(), N_SIZE);
}

TEST(TestDirectedGraph, IsDirected) {
    DirectedGraph g(N);
    ASSERT_TRUE(g.is_directed());
}

TEST(TestDirectedGraph, IsDag) {
    FAIL();
}

TEST(TestDirectedGraph, ToUndirected) {
    DirectedGraph g(N);
    Graph ug = g.to_undirected();
    ASSERT_EQ(g.size(), ug.size());
    ASSERT_FALSE(ug.is_directed());
}
