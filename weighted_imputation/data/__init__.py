import sys
from os import listdir
from os.path import abspath, basename, dirname, isfile, join, splitext
from typing import Dict

from ..structures import BayesianNetwork, Dataset

NETWORKS = abspath(join(dirname(__file__), 'networks'))
NETWORKS = [join(NETWORKS, network) for network in listdir(NETWORKS)]
NETWORKS = [
    network
    for network in NETWORKS
    if isfile(network) and network.endswith('.bif')
]
NETWORKS = {
    splitext(basename(network))[0] : network
    for network in NETWORKS
}

DATASETS = abspath(join(dirname(__file__), 'datasets'))
DATASETS = [join(DATASETS, dataset) for dataset in listdir(DATASETS)]
DATASETS = [dataset for dataset in DATASETS if isfile(dataset)]
DATASETS = {
    splitext(basename(dataset))[0] : dataset
    for dataset in DATASETS
}

def load_networks_from_disk() -> Dict:
    return {
        key : BayesianNetwork.from_file(value)
        for key, value in NETWORKS.items()
    }

def load_datasets_from_disk() -> Dict:
    return {
        key: Dataset.from_file(value)
        for key, value in DATASETS.items()
    }

for key, value in load_networks_from_disk().items():
    setattr(sys.modules[__name__], key, value)
