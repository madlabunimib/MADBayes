#pragma once

#include <structures/bayesian_network.ipp>

namespace madbayes {

using Factor = DataArray;

struct Clique {
    bool is_separator;
    Nodes nodes;
    Factor belief;
};

using Cliques = std::vector<Clique>;

namespace algorithms {

using namespace madbayes::structures;

class CliqueTree : public Graph {
   private:
    std::map<Node, Clique> label2clique;

    std::string clique2label(const Clique &clique);
    std::vector<Clique> build_cliques(const BayesianNetwork &bn);
    void build_clique_tree(const Cliques &cliques);

   public:
    CliqueTree(const BayesianNetwork &bn);
    CliqueTree(const CliqueTree &other);
    CliqueTree &operator=(const CliqueTree &other);
    ~CliqueTree();
};

}  // namespace algorithms

}  // namespace madbayes
