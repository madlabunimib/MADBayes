import pandas as pd


class Dataset:

    def __init__(self, dataset: pd.DataFrame):
        self.data = dataset

    def absolute_frequencies(self, columns=None):
        if columns is None or len(columns) == 0:
            columns = list(self.data.columns)
        return self.data.groupby(columns).size().to_frame('count')

    @classmethod
    def from_file(cls, path: str):
        dataset = pd.read_csv(
            path,
            sep=',',
            header=0
        )
        return cls(dataset)
