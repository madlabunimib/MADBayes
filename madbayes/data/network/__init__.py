import sys
from os import listdir
from os.path import abspath, basename, dirname, isfile, join, splitext
from typing import Dict

from ...structures import BayesianNetwork

NETWORKS = abspath(dirname(__file__))
NETWORKS = [join(NETWORKS, network) for network in listdir(NETWORKS)]
NETWORKS = [
    network
    for network in NETWORKS
    if isfile(network) and network.endswith('.bif')
]
NETWORKS = {
    splitext(basename(network))[0]: network
    for network in NETWORKS
}


def load_networks_from_disk() -> Dict:
    return {
        key: BayesianNetwork.from_file(value)
        for key, value in NETWORKS.items()
    }


for key, value in load_networks_from_disk().items():
    setattr(sys.modules[__name__], key, value)
