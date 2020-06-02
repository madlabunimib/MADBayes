import numpy as np
from math import isclose
from . import weighted_imputation as wi


def test_hc():
    wi.utils.rpy2_init()
    datasets = wi.data.dataset.DATASETS
    datasets_networks = [
        (
            getattr(wi.data.dataset, dataset),
            datasets[dataset]
        )
        for dataset, _ in datasets.items()
        if dataset in ['asia', 'cancer', 'earthquake', 'sachs', 'survey']
    ]
    for dataset, dataset_path in datasets_networks:
        df = wi.utils.rpy2.utils.read_csv(dataset_path)
        dag_bn = wi.utils.rpy2.bnlearn.hc(df, score='bds')
        dag_bn = wi.utils.rpy2.bnlearn.model2network(wi.utils.rpy2.bnlearn.modelstring(dag_bn))
        score_bn = wi.utils.rpy2.bnlearn.score(dag_bn, df, type='bds')
        score_bn = np.array(score_bn)[0]
        dag_python = wi.hill_climbing(dataset)
        score_python = wi.bds_score(dag_python, dataset)
        assert(isclose(score_bn, score_python))
