import sys
from os import listdir
from os.path import abspath, basename, dirname, isfile, join, splitext
from typing import Dict

from ...structures import Dataset

DATASETS = abspath(dirname(__file__))
DATASETS = [join(DATASETS, dataset) for dataset in listdir(DATASETS)]
DATASETS = [dataset for dataset in DATASETS if isfile(dataset)]
DATASETS = {
    splitext(basename(dataset))[0]: dataset
    for dataset in DATASETS
    if isfile(dataset) and dataset.endswith('.csv')
}


def load_datasets_from_disk() -> Dict:
    return {
        key: Dataset.from_csv(value)
        for key, value in DATASETS.items()
    }


for key, value in load_datasets_from_disk().items():
    setattr(sys.modules[__name__], key, value)
