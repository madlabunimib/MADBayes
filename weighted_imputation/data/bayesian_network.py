from os import listdir
from os.path import abspath, basename, dirname, isfile, join, splitext
from typing import Dict

from ..structures import BayesianNetwork


def load_networks_from_disk() -> Dict:
    networks = abspath(join(dirname(__file__), '../networks'))
    networks = [join(networks, network) for network in listdir(networks)]
    networks = [network for network in networks if isfile(network) and network.endswith('.bif')]

    networks = {
        splitext(basename(network))[0] : BayesianNetwork.from_file(network)
        for network in networks
    }

    return networks
