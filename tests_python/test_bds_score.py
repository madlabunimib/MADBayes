import numpy as np
import rpy2.robjects as robjects
from math import isclose
from . import weighted_imputation as wi

def test_bds_score():
    wi.utils.rpy2_init()
    datasets = wi.data.dataset.DATASETS
    networks = wi.data.network.NETWORKS
    datasets_networks = [
        (
            getattr(wi.data.dataset, dataset),
            datasets[dataset],
            getattr(wi.data.network, dataset),
            networks[dataset]
        )
        for dataset, _ in datasets.items()
    ]
    for dataset, dataset_path, network, network_path in datasets_networks:
        df = wi.utils.rpy2.utils.read_csv(dataset_path)
        bn = wi.utils.BNLearnNetwork.from_bif(network_path)
        bds_python, bds_python_nodes = wi.bds_score(network, dataset, with_nodes=True)
        bds_r = wi.utils.rpy2.bnlearn.score(bn.as_bn(), df, type = "bds", by_node = True)
        bds_r = dict(zip(bds_r.names, list(bds_r)))
        for k, v in bds_python_nodes.items():
            assert(isclose(v, bds_r[k]))
