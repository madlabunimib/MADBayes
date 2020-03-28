import sys
from .bayesian_network import load_networks_from_disk

for key, value in load_networks_from_disk().items():
    setattr(sys.modules[__name__], key, value)
