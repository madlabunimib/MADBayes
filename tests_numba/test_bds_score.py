import numpy as np
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
        bds_python = wi.bds_score(network, dataset)
        bds_r = wi.utils.rpy2.bnlearn.score(bn.as_bn(), df, type = "bds")
        bds_r = np.array(bds_r)[0]
        assert(isclose(bds_python, bds_r))
