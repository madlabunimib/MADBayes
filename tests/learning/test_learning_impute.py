import numpy as np
from . import madbayes as mb


def test_learning_impute():
    datasets = mb.data.dataset.DATASETS
    networks = mb.data.network.NETWORKS
    datasets_networks = [
        (
            getattr(mb.data.dataset, dataset),
            getattr(mb.data.network, dataset)
        )
        for dataset, _ in datasets.items()
        if dataset in ['asia', 'cancer', 'earthquake', 'sachs', 'survey']
    ]
    for (dataset, network) in datasets_networks:
        imputed = mb.impute(network, dataset.random_nan(), mb.JunctionTree)
        tot = np.prod(dataset.data.shape)
        err = np.count_nonzero(
            dataset.data.values == imputed.data.values
        )
        err = 1 - (err / tot)
        assert(err < 0.10)
