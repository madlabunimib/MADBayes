from itertools import combinations
from random import choice, randint, sample
from xarray.testing import assert_allclose
from . import madbayes as mb

def test_junction_tree():
    networks = dir(mb.data.network)
    networks = [
        getattr(mb.data.network, network)
        for network in networks
    ]
    networks = [
        network
        for network in networks
        if isinstance(network, mb.BayesianNetwork)
    ]
    assert(len(networks) > 0)
    jts = [
        mb.junction_tree(network)
        for network in networks
    ]

def test_junction_tree_query():
    mb.utils.rpy2_init()
    networks = ['asia', 'cancer', 'earthquake', 'sachs', 'survey']
    networks = {
        name: path
        for name, path in mb.data.network.NETWORKS.items()
        if name in networks
    }
    for name, path in networks.items():
        jt_0 = getattr(mb.data.network, name)
        # Nodes of the bayesian network
        nodes = list(jt_0.nodes())
        levels = {
            node: [
                str(level)
                for level in jt_0.levels(node)
            ]
            for node in nodes
        }
        # Build junction tree
        jt_0 = mb.junction_tree(jt_0)
        # Load bnlearn and grain
        jt_1 = mb.utils.BNLearnNetwork.from_bif(path)
        jt_1 = mb.utils.gRainJunctionTree(jt_1)
        # Generate random queries
        queries = [
            list(query)
            for i in range(1, len(nodes))
            for query in combinations(nodes, i)
        ]
        queries = sample(queries, int(len(queries) * 0.3))
        # Generate random evidence for each query
        evidences = [
            list(set(nodes).difference(set(query)))
            for query in queries
        ]
        evidences = [
            sample(evidence, randint(1, len(evidence)))
            for evidence in evidences
        ]
        evidences = [
            {
                variable : choice(levels[variable])
                for variable in evidence
            }
            for evidence in evidences
        ]
        # Select the query method
        methods = ['marginal', 'joint', 'conditional']
        queries = [
            {
                'variables': query,
                'method': choice(methods)
            }
            for query in queries
        ]
        # Execute the query
        for i, query in enumerate(queries):
            evidence = evidences[i]
            jte_0 = jt_0.set_evidence(**evidence)
            jte_1 = jt_1.set_evidence(**evidence)
            out_0 = jte_0.query(query['method'], query['variables'])
            out_1 = jte_0.query(query['method'], query['variables'])
            for j, _ in enumerate(out_0):
                assert_allclose(out_0[j], out_1[j])
