#pragma once

#include <structures/probability_table.ipp>

namespace madbayes {

using Factor = DataArray;

struct Clique {
    bool is_separator;
    Nodes nodes;
    Factor belief;

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

namespace algorithms {

using namespace madbayes::structures;

class CliqueTree : public Graph {
   private:
    std::map<Node, Clique> label2clique;

    template <typename T>
    Cliques build_cliques(const T &other);
    void build_clique_tree(const Cliques &cliques);
    Factor calibrate_upward(const Node &prev, const Node &curr);
    void calibrate_downward(const Node &prev, const Node &curr, const Factor &message);

   public:
    template <typename T>
    CliqueTree(const T &other);
    CliqueTree(const CliqueTree &other);
    CliqueTree &operator=(const CliqueTree &other);
    ~CliqueTree();

    Clique get_clique(const Node &label) const;
    void set_clique(const Clique &clique);

    Clique get_clique_given_variables(const Nodes &variables) const;
    Factor get_joint_query(const Node &prev, const Node &curr, Nodes *variables) const;
};

}  // namespace algorithms

}  // namespace madbayes
