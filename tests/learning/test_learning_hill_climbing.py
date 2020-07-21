import numpy as np
from math import isclose
from . import madbayes as mb


def test_learning_hill_climbing():
    mb.utils.rpy2_init()
    datasets = mb.data.dataset.DATASETS
    datasets_networks = [
        (
            getattr(mb.data.dataset, dataset),
            datasets[dataset]
        )
        for dataset, _ in datasets.items()
        if dataset in ['asia', 'cancer', 'earthquake', 'sachs', 'survey']
    ]
    for dataset, dataset_path in datasets_networks:
        df = mb.utils.rpy2.utils.read_csv(dataset_path)
        dag_bn = mb.utils.rpy2.bnlearn.hc(df, score='bds')
        dag_bn = mb.utils.rpy2.bnlearn.model2network(mb.utils.rpy2.bnlearn.modelstring(dag_bn))
        score_bn = mb.utils.rpy2.bnlearn.score(dag_bn, df, type='bds')
        score_bn = np.array(score_bn)[0]
        dag_python = mb.hill_climbing(dataset)
        score_python = mb.bds_score(dag_python, dataset)
        assert(isclose(score_bn, score_python))
