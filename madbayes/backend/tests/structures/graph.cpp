#include <gtest/gtest.h>

#include "structures/graph.ipp"

#define N {"1", "2", "3", "4", "5"}
#define N_SIZE 5

using namespace madbayes::structures;

TEST(TestGraph, DefaultContructor) {
    Graph g(N);
    ASSERT_EQ(g.size(), N_SIZE);
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
    ASSERT_EQ(g->size(), N_SIZE);
    delete g;
}

TEST(TestGraph, PointerContructor) {
    igraph_t ig;
    igraph_empty(&ig, N_SIZE, IGRAPH_UNDIRECTED);
    Graph g(&ig);
    ASSERT_EQ(g.size(), N_SIZE);
}

TEST(TestGraph, GetNodes) {
    Graph g(N);
    ASSERT_EQ(g.get_nodes(), Nodes(N));
}

TEST(TestGraph, SetNodes) {
    Graph g(N);
    g.set_nodes(N);
    ASSERT_EQ(g.get_nodes(), Nodes(N));
}

TEST(TestGraph, Size) {
    Graph g(N);
    ASSERT_EQ(g.size(), N_SIZE);
}

TEST(TestGraph, IsDirected) {
    Graph g(N);
    ASSERT_FALSE(g.is_directed());
}
