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
        imputed = mb.impute(mb.JunctionTree(network), dataset.random_nan())
        tot = np.prod(dataset.shape)
        err = np.count_nonzero(
            dataset.values == imputed.values
        )
        err = 1 - (err / tot)
        assert(err < 0.10)
