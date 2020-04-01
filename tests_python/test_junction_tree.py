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
