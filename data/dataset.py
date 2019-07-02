"""Dataset class for CHSI dataset that can be extended by dataset-specific classes."""
from pathlib import Path
import pandas as pd


class Dataset(pd.DataFrame):

    def __init__(self, filename=None):
        """
        pandas Dataframe with methods to extract certain column features
        from CHSI datasets.  Also contain self loading and preprocessing
        methods.
        Parameters
        ----------
        filename : csv filename that contains CHSI data
        """
        self.df = self.load_data(filename)
        self.filename = filename

    @classmethod
    def load_data(self, filename=None):
        return pd.read_csv(filename)

    def preproc(self):
        """
        Preprocessing CHSI dataset.  First, dropping the confidence interval
        columns that starts with 'CI_'.  Then changing some invalid values to
        np.nan according to DEFINEDDATAVALUE.csv. Also constructs the five digit
        FIPS code from State_FIPS_Code and County_FIPS_Code.
        """
        cols = self._data.columns.values
        cols_drop = [c for c in cols if 'CI_' in c]
        self.df = self.df.drop(self.df[cols_drop], axis=1)

        self.df = self.df.replace([-1,-1111,-1111.1,-2,-2222.2,-2222,-9999,-9989.9],
                      [np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan])

        self.df['FIPS'] = self.df['State_FIPS_Code'].apply(lambda x:str(x).zfill(2)) +
                          self.df['County_FIPS_Code'].apply(lambda x:str(x).zfill(3))
        return None

    def lookup(self, age, race, cod) -> pd.DataFrame:
        """
        Takes in age, race, cod as argument and returns a dataframe slice from
        the CHSI dataset with the FIPS column and feature column.
        """
        feature_col = str(age)+'_'+str(race)+'_'+str_cod
        print(feature_col)
        return self.df[['FIPS', feature_col]]
