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

    def levels(self):
        return {
            column: sorted(self.data[column].dropna().unique())
            for column in self.data.columns
        }

    def random_nan(self, nan_rows_rate: float = 0.2, max_nan_per_row: int = 2):
        data = self.data.copy()
        rows, cols = self.data.shape
        rows = sample(range(rows), min([int(rows * nan_rows_rate), rows]))
        rows = [
            (i, j)
            for i in rows
            for j in sample(range(cols), min([max_nan_per_row, cols]))
        ]
        for i, j in rows:
            data.iloc[[i], [j]] = np.nan
        return type(self)(data)

    def to_dict(self):
        return self.data.to_dict('records')

    @classmethod
    def from_file(cls, path: str):
        dataset = pd.read_csv(
            path,
            sep=',',
            header=0,
            dtype=str
        )
        return cls(dataset)

    def __repr__(self):
        return super().__repr__()
