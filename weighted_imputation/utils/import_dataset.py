import pandas as pd
from typing import Dict

def import_dataset(dataset_path: str) -> pd.DataFrame:
    return pd.read_csv(dataset_path)

def get_frequencies(dataset: pd.DataFrame) -> Dict:
    frequencies = {}
    for field in dataset.columns:
        tmp = dataset[field].value_counts(normalize = True).to_dict()
        frequencies.update({field: {}})
        for key in tmp.keys():
            frequencies[field].update({key : tmp[key]})
    return frequencies


def get_frequencies_of_clique(dataset: pd.DataFrame, clique_structure: str):

    return