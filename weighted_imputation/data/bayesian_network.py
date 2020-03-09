from os.path import abspath, dirname, join
from ..structures import BayesianNetwork

DATASETS = abspath(join(dirname(__file__), '../datasets'))
NETWORKS = abspath(join(dirname(__file__), '../networks'))

asia = BayesianNetwork.from_file_and_dataset(
    join(NETWORKS, 'asia.bif'),
    join(DATASETS, 'asia.csv')
)
