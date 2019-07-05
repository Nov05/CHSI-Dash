"""Dataset class for CHSI dataset that can be extended by dataset-specific classes."""
from pathlib import Path
import pandas as pd
import numpy as np
import bottleneck as bn

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
        return self.df[['FIPS', feature_col]]

    def isin_cols(self, age, race, cod):
        """
        Takes in age, race, cod as argument and returns a boolean value that
        flags if the age, race, cod combination exists in the dataframe.
        """
        feature_col = str(age)+'_'+str(race)+'_'+str(cod)
        cols = self.df.columns.values
        return feature_col in cols

    def state_data(self) -> pd.DataFrame:
        """
        Extracting State data for injury, homicide for all ethnicities.
        Adopted from George's Notebook.

        NOTE: Has to be called w/o preproc()
        """
        CI_cols = [col for col in self.df.columns if 'CI_' in col]
        df_clean = self.df.drop(self.df[CI_cols],axis=1)
        # replace negative values with NaN
        df_clean = df_clean.replace([-1,-1111,-1111.1,-2,-2222.2,-2222,-9999,-9989.9],
                          [np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,
                          np.nan])

        death_data = []
        # list of all causes of death
        cause_lst = df_clean.columns[6:-1]
        # list and sort all states
        state_col = np.array(df_clean.CHSI_State_Name.value_counts().index)
        state_col.sort()
        # create mean value of all causes in all states
        for state in state_col:
            df_state = df_clean[df_clean['CHSI_State_Name']==state]
            FIPS_Code = df_state.iloc[-1].State_FIPS_Code
            state_abbr = df_state.iloc[-1].CHSI_State_Abbr
            state_lst = [FIPS_Code, state, state_abbr]
            cause_mean = []
            for cause in cause_lst:
                cause_mean.append(df_state[cause].mean())
            state_lst.extend(cause_mean)
            death_data.append(state_lst)

        # create dataframe for mean % of causes of death in all states
        chsi_cols = ['State_FIPS_Code','State_Name','State_Abbr']
        chsi_cols.extend(cause_lst)
        df_mean = pd.DataFrame(death_data, columns=chsi_cols)

        comp_cols = [col for col in df_mean.columns if '_Comp' in col or
             '_BirthDef' in col or '_Cancer' in col or '_HeartDis' in col]
        df_drop = df_mean.drop(df_mean[comp_cols],axis=1)
        print(df_drop.columns)
        print(df_drop.head(5))

        group = df_drop.columns[3:]
        # list and sort all states
        state_col = np.array(df_drop.State_Name.value_counts().index)
        state_col.sort()
        age_groups = ['B_','C_','D_']
        causes_lst = ['_Injury','_Homicide','_Suicide','_HIV']
        # create causes of death data
        death_data = []
        # create mean value of all causes in all states
        for state in state_col:
          df_state = df_drop[df_drop['State_Name']==state]
          FIPS_Code = df_state.iloc[0].State_FIPS_Code
          state_abbr = df_state.iloc[0].State_Abbr
          state_lst = [FIPS_Code, state, state_abbr]
          cause_mean = []
          for age in age_groups:
            for cause in causes_lst:
              cause_pct = []
              i = 0
              for sub in group:
                if age in sub and cause in sub:
                  i += 1
                  cause_pct.append(df_state.iloc[0][sub])
              if i > 0:
                cause_mean.append(bn.nanmean(cause_pct))
          state_lst.extend(cause_mean)
          death_data.append(state_lst)

        print(len(death_data))
        # create dataframe for mean % of causes of death in all states
        chsi_cols = ['State_FIPS_Code','State_Name','State_Abbr','B_Injury','B_Homicide'
                    ,'C_Injury','C_Homicide','C_Suicide','D_Injury','D_Homicide'
                    ,'D_Suicide','D_HIV']
        df = pd.DataFrame(death_data,columns=chsi_cols)
        #print(df.shape)
        #df
        #feature_col = str(age)+'_'+str(race)+'_'+str(cod)
        return df
