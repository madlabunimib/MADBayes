import numpy as np
import pandas as pd


class Dataset(pd.DataFrame):

    def absolute_frequency(self, columns=None):
        if columns is None or len(columns) == 0:
            columns = list(self.columns)
        return self.groupby(columns, dropna=False).size().to_frame('count')

    def levels(self, variable=None):
        if variable is None:
            return {
                column: sorted(self[column].dropna().unique())
                for column in self.columns
            }
        return sorted(self[variable].dropna().unique())
    
    def count_nan(self) -> int:
        return self.size - self.count().sum()

    def random_nan(self, ratio: float = 0.20, columns=None):
        data = self.copy()
        if columns is None:
            data = data.mask(np.random.random(data.shape) < ratio)
        else:
            shape = data[columns].shape
            data[columns] = data[columns].mask(np.random.random(shape) < ratio)
        return type(self)(data)

    def to_dict(self):
        return super().to_dict('records')

    @classmethod
    def from_csv(cls, path: str):
        dataset = pd.read_csv(
            path,
            sep=',',
            header=0,
            dtype=str
        )
        return cls(dataset)
