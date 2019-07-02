"""Dataset class that can be extended by dataset-specific classes."""
from pathlib import Path
import pandas as pd
#import os


class Dataset(pd.DataFrame):

    def __init__(self, filename=None):
        """
        pandas Dataframe with methods to extract certain column features
        from CHSI datasets.  Also contain self loading and preprocessing
        methods.
        """
        self._data = self.load_data(filename)
        self.filename = filename

    @classmethod
    def load_data(self, filename=None):
        return pd.read_csv(filename)

    def preproc(self):
        # dropping confidence interval columns. Confidence interval columns
        # starting with 'CI_'
        cols = self._data.columns.values
        cols_drop = [c for c in cols if 'CI_' in c]
        self._data = self._data.drop(self._data[cols_drop], axis=1)

        self._data = self._data.replace([-1111, -2222], [np.nan, np.nan])
        return None

    def extract(self, age, race, cod):
        feature_col = str(age)
        return
