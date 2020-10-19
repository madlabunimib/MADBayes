from itertools import chain, combinations, product
from random import choices
from xarray.testing import assert_allclose
from . import madbayes as mb

def test_inference_junction_tree():
    networks = ['asia', 'earthquake', 'survey']
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
        mb.JunctionTree(network)
        for network in networks
    ]

def test_inference_junction_tree_query():
    mb.utils.rpy2_init()
    networks = ['asia', 'earthquake', 'survey']
    networks = {
        name: path
        for name, path in mb.data.network.NETWORKS.items()
        if name in networks
    }
    for name, path in networks.items():
        jt_0 = getattr(mb.data.network, name)
        # Nodes of the bayesian network
        nodes = jt_0.nodes
        levels = {
            node: jt_0.get_levels(node)
            for node in nodes
        }
        # Build junction tree
        jt_0 = mb.JunctionTree(jt_0)
        # Load bnlearn and grain
        jt_1 = mb.utils.gRainJunctionTree.from_bif(path)
        # Generate random queries
        queries = [
            dict(zip(levels.keys(), q))
            for q in product(*levels.values())
        ]

        def powerset(s):
            return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))
        
        select = powerset(nodes)
        select = [list(s) for s in select]
        select = [s for s in select if len(s) > 0 and len(s) < len(nodes)]

        queries = [
            {
                "variables": s,
                "evidence": {
                    k: v for (k, v) in q.items()
                    if k not in s
                },
                "method": method
            }
            for q in queries
            for s in select
            for method in ["marginal", "joint", "conditional"]
        ]

        queries = choices(queries, k = int(len(queries) * 0.01))

        # Execute the query
        for query in queries:
            from rpy2.rinterface_lib.embedded import RRuntimeError
            try:
                out_0 = jt_0.query(**query)
                out_1 = jt_1.query(**query)
                for j, _ in enumerate(out_0):
                    assert_allclose(out_0[j], out_1[j].fillna(0))
            except RRuntimeError:
                pass
            except KeyError:
                pass
