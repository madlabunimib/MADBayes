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

TEST(TestDirectedGraph, FormulaConstructor) {
    Nodes nodes = {"A", "B", "C", "D"};
    Edges edges = {
        {"A", "B"},
        {"A", "C"},
        {"B", "C"},
        {"A", "D"},
        {"B", "D"},
        {"C", "D"}
    };
    DirectedGraph g("[A][B|A][C|A:B][D|A:B:C]");
    ASSERT_EQ(g.get_nodes(), nodes);
    ASSERT_EQ(g.get_edges(), edges);
}

TEST(TestDirectedGraph, EdgesConstructor) {
    Nodes nodes = {"A", "B", "C", "D"};
    Edges edges = {
        {"A", "B"},
        {"A", "C"},
        {"B", "C"},
        {"A", "D"},
        {"B", "D"},
        {"C", "D"}
    };
    DirectedGraph g(edges);
    ASSERT_EQ(g.get_nodes(), nodes);
    ASSERT_EQ(g.get_edges(), edges);
}

TEST(TestDirectedGraph, IsDirected) {
    DirectedGraph g(N);
    ASSERT_TRUE(g.is_directed());
}

TEST(TestDirectedGraph, IsDag) {
    DirectedGraph g0("[A|B][B|A]"), g1("[A|B][B|C]");
    ASSERT_FALSE(g0.is_dag());
    ASSERT_TRUE(g1.is_dag());
}

TEST(TestDirectedGraph, FromUndirected) {
    Graph ug(N);
    DirectedGraph g(ug);
    ASSERT_EQ(g.size(), ug.size());
    ASSERT_TRUE(g.is_directed());
}

TEST(TestDirectedGraph, ToUndirected) {
    DirectedGraph g(N);
    Graph ug = g.to_undirected();
    ASSERT_EQ(g.size(), ug.size());
    ASSERT_FALSE(ug.is_directed());
}

TEST(TestDirectedGraph, Parents) {
    DirectedGraph g("[A|B:C:D]");
    ASSERT_EQ(g.parents("A"), Nodes({"B", "C", "D"}));
}

TEST(TestDirectedGraph, Family) {
    DirectedGraph g("[A|B:C:D]");
    ASSERT_EQ(g.family("A"), Nodes({"B", "C", "D", "A"}));
}

TEST(TestDirectedGraph, Children) {
    DirectedGraph g("[A][B|A][C|A][D|A]");
    ASSERT_EQ(g.children("A"), Nodes({"B", "C", "D"}));
}

TEST(TestDirectedGraph, Ancestrors) {
    DirectedGraph g("[A][B|A][C|B][D|C]");
    ASSERT_EQ(g.ancestors("D"), Nodes({"A", "B", "C"}));
}

TEST(TestDirectedGraph, Descendants) {
    DirectedGraph g("[A][B|A][C|B][D|C]");
    ASSERT_EQ(g.descendants("A"), Nodes({"B", "C", "D"}));
}
