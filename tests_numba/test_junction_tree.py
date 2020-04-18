from itertools import combinations
from random import choice, randint, sample
from xarray.testing import assert_allclose
from . import weighted_imputation as wi

def test_junction_tree():
    networks = dir(wi.data)
    networks = [
        getattr(wi.data, network)
        for network in networks
    ]
    networks = [
        network
        for network in networks
        if isinstance(network, wi.BayesianNetwork)
    ]
    assert(len(networks) > 0)
    jts = [
        wi.junction_tree(network)
        for network in networks
    ]

def test_junction_tree_query():
    wi.utils.rpy2_init()
    for name, path in wi.data.NETWORKS.items():
        jt_0 = getattr(wi.data, name)
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
        jt_0 = wi.junction_tree(jt_0)
        # Load bnlearn and grain
        jt_1 = wi.utils.BNLearnNetwork.from_bif(path)
        jt_1 = wi.utils.gRainJunctionTree(jt_1)
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
