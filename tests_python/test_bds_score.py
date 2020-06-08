import numpy as np
import rpy2.robjects as robjects
from os.path import abspath, dirname, join
from math import log, isclose
from . import madbayes as mb

def test_bds_score():
    mb.utils.rpy2_init()
    datasets = mb.data.dataset.DATASETS
    networks = mb.data.network.NETWORKS
    datasets_networks = [
        (
            getattr(mb.data.dataset, dataset),
            datasets[dataset],
            getattr(mb.data.network, dataset),
            networks[dataset]
        )
        for dataset, _ in datasets.items()
    ]
    for dataset, dataset_path, network, network_path in datasets_networks:
        df = mb.utils.rpy2.utils.read_csv(dataset_path)
        bn = mb.utils.BNLearnNetwork.from_bif(network_path)
        bds_python, bds_python_nodes = mb.bds_score(network, dataset, with_nodes=True)
        bds_r = mb.utils.rpy2.bnlearn.score(bn.as_bn(), df, type = "bds", by_node = True)
        bds_r = dict(zip(bds_r.names, list(bds_r)))
        for k, v in bds_python_nodes.items():
            assert(isclose(v, bds_r[k]))


def test_bds_score_suzuki_2016():
    refs = [
        '../test_data/suzuki_2016_1.csv',
        '../test_data/suzuki_2016_2.csv'
    ]
    refs = [abspath(join(dirname(__file__), ref)) for ref in refs]
    refs = [mb.Dataset.from_csv(ref) for ref in refs]
    dags = ['[X|Z:W][Z][W][Y]', '[X|Z:W:Y][Z][W][Y]']
    outs = [log(0.03262539), log(3.90625e-07)]

    for i, ref in enumerate(refs):
        for dag in dags:
            _, nodes = mb.bds_score(dag, ref, with_nodes=True)
            assert(isclose(
                nodes['X'],
                outs[i],
                rel_tol=1e-8,
                abs_tol=1e-8
            ))
