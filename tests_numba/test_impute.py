import numpy as np
from . import weighted_imputation as wi


def test_impute():
    datasets = wi.data.dataset.DATASETS
    networks = wi.data.network.NETWORKS
    datasets_networks = [
        (
            getattr(wi.data.dataset, dataset),
            getattr(wi.data.network, dataset)
        )
        for dataset, _ in datasets.items()
        if dataset in ['asia', 'cancer', 'earthquake', 'sachs', 'survey']
    ]
    for (dataset, network) in datasets_networks:
        imputed = wi.impute(network, dataset.random_nan())
        tot = np.prod(dataset.data.shape)
        err = np.count_nonzero(
            dataset.data.values == imputed.data.values
        )
        err = 1 - (err / tot)
        assert(err < 0.10)
