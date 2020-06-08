import numpy as np
import pandas as pd

from random import sample


class Dataset:

    def __init__(self, dataset: pd.DataFrame):
        self.data = dataset

    def absolute_frequencies(self, columns=None):
        if columns is None or len(columns) == 0:
            columns = list(self.data.columns)
        return self.data.groupby(columns).size().to_frame('count')

    def columns(self):
        return list(self.data.columns)

    def levels(self, variable=None):
        if variable is None:
            return {
                column: sorted(self.data[column].dropna().unique())
                for column in self.data.columns
            }
        return sorted(self.data[variable].dropna().unique())

    def random_nan(self, ratio: float = 0.20):
        data = self.data.copy()
        data = data.mask(np.random.random(data.shape) < ratio)
        return type(self)(data)

    def to_dict(self):
        return self.data.to_dict('records')

    @classmethod
    def from_csv(cls, path: str):
        dataset = pd.read_csv(
            path,
            sep=',',
            header=0,
            dtype=str
        )
        return cls(dataset)

    def __repr__(self):
        return super().__repr__()
