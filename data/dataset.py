"""Dataset class for CHSI dataset that can be extended by dataset-specific classes."""
from pathlib import Path
import pandas as pd
import numpy as np


class Dataset():

    def __init__(self, filename=None):
        """
        pandas Dataframe with methods to extract certain column features
        from CHSI datasets. Inits with self loading csv. Also contains
        preprocessing methods.

        Parameters
        ----------
        filename : csv filename that contains CHSI data
        """
        self.df = pd.read_csv(filename)
        self.filename = filename

    def preproc(self):
        """
        Preprocessing CHSI dataset. First, dropping the confidence interval
        columns that starts with 'CI_'. Then changing some invalid values to
        np.nan according to DEFINEDDATAVALUE.csv. Also constructs the five digit
        FIPS code from State_FIPS_Code and County_FIPS_Code.

        TODO: plotly throws unrecognized FIPS value [2280]. Can't seem to find
        that exact value looking at df.FIPS.
        """
        cols = self.df.columns.values
        cols_drop = [c for c in cols if 'CI_' in c]
        self.df = self.df.drop(self.df[cols_drop], axis=1)
        self.df = self.df.replace([-1,-1111,-1111.1,-2,-2222.2,-2222,-9999,-9989.9],
                      [np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan])

        self.df.State_FIPS_Code = self.df.State_FIPS_Code.apply(lambda x:str(int(x)).zfill(2))
        self.df.County_FIPS_Code = self.df.County_FIPS_Code.apply(lambda x:str(int(x)).zfill(3))

        self.df['FIPS'] = self.df.State_FIPS_Code + self.df.County_FIPS_Code
        #print(self.df[self.df['FIPS'].str.contains("2280")])
        #print(self.df.FIPS)#self.df.FIPS.astype('int').describe())

    def lookup(self, age, race, cod) -> pd.DataFrame:
        """
        Takes in age, race, cod as argument and returns a dataframe slice from
        the CHSI dataset with the FIPS column and feature column.
        """
        feature_col = str(age)+'_'+str(race)+'_'+str(cod)
        print(feature_col)
        return self.df[['FIPS', feature_col]]

    def isin_cols(self, age, race, cod):
        """
        Takes in age, race, cod as argument and returns a boolean value that
        flags if the age, race, cod combination exists in the dataframe.
        """
        feature_col = str(age)+'_'+str(race)+'_'+str(cod)
        cols = self.df.columns.values
        #print(feature_col)
        return feature_col in cols
