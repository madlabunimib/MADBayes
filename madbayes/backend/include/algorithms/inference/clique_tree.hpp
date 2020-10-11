#pragma once

#include <algorithms/structure/chain_cliques.ipp>
#include <algorithms/structure/chordal.ipp>
#include <algorithms/structure/maximal_cliques.ipp>
#include <algorithms/structure/maximum_cardinality_search.ipp>
#include <algorithms/structure/moral.ipp>
#include <structures/discrete_bayesian_network.hpp>
#include <structures/data_array.hpp>

namespace madbayes {

namespace algorithms {

using namespace madbayes::structures;

struct Clique {
    bool is_separator;
    Nodes nodes;
    DataArray belief;

    operator std::string() const {
        std::stringstream out;
        out << '{' << nodes[0];
        for (size_t i = 1; i < nodes.size(); i++) {
            out << ',' << nodes[i];
        }
        out << '}';
        return out.str();
    }
};

using Cliques = std::vector<Clique>;

class CliqueTree : public Graph {
   private:
    std::map<Node, Clique> label2clique;

    template <typename T>
    Cliques build_cliques(const T &other);
    void build_clique_tree(const Cliques &cliques);

   public:
    template <typename T>
    CliqueTree(const T &other);
    CliqueTree(const CliqueTree &other);
    CliqueTree &operator=(const CliqueTree &other);
    ~CliqueTree();

    Clique get_clique(const Node &label) const;
    void set_clique(const Clique &clique);

    std::vector<DataArray> query(const Nodes &variables, const Evidence &evidence, const std::string &method) const;

    DataArray calibrate_upward(const Node &prev, const Node &curr);
    void calibrate_downward(const Node &prev, const Node &curr, DataArray message);
    void absorb_evidence(const Evidence &evidence);

    Clique get_clique_given_variables(const Nodes &variables) const;
    DataArray get_joint_query(const Node &prev, const Node &curr, Nodes *variables) const;
};

}  // namespace algorithms

}  // namespace madbayes
