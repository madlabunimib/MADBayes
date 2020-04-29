import pandas as pd


class Dataset:

    def __init__(self, dataset: pd.DataFrame):
        self.data = dataset

    def absolute_frequencies(self):
        return self.data.groupby(list(self.data.columns)).size().reset_index(name='count')

    def absolute_frequencies_sublist(self, columns: list):
        return self.data.groupby(columns).size().reset_index(name='count')

    @classmethod
    def from_file(cls, path: str):
        dataset = pd.read_csv(
            path,
            sep=',',
            header=0
        )
        return cls(dataset)
