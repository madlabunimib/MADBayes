import pandas as pd


class Dataset:

    def __init__(self, dataset: pd.DataFrame):
        self.data = dataset

    def absolute_frequencies(self):
        return self.data.groupby(list(self.data.columns)).size().reset_index(name='count')
    
    def levels(self):
        return {
            column : sorted(self.data[column].dropna().unique())
            for column in self.data.columns
        }
    
    def to_dict(self):
        return self.data.to_dict('records')

    @classmethod
    def from_file(cls, path: str):
        dataset = pd.read_csv(
            path,
            sep=',',
            header=0
        )
        return cls(dataset)
