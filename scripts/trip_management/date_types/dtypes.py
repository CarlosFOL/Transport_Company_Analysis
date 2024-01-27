from ..trip_dates import TripDates
import pandas as pd

class DateTypes(TripDates):
    
    def customized_dtypes(self, dtype_dd: type, dtype_ad: type) -> pd.DataFrame:
        """
        Filter the dates according to 
        the dtype selected for the 
        departure and arrival dates
        """
        dtypes_selected = self.table.apply(
        lambda x: type(x['FECHA DE INICIO']) == dtype_dd
        and type(x['FECHA DE LLEGADA']) == dtype_ad, axis = 1
        )
        return self.table.loc[dtypes_selected, :]

class SingleDtype(TripDates):
    def __init__(self, df_tc: pd.DataFrame, dtype: type) -> None:
        super().__init__(df_tc)
        self.dtype = dtype
    
    @property
    def dtype_table(self) -> pd.DataFrame:
        """
        It contains the trips whose 
        departure or arrival date is 
        of the dtype selected by the user
        """
        df_dtypes = self.table.map(type)
        cond_type = df_dtypes.isin([self.dtype]).sum(axis=1).map(bool)
        return df_dtypes[cond_type]

    def __pairs_grouping(self) -> pd.DataFrame:
        """
        Get the pairs where at least one is 
        of the dtype selected. Then, group the 
        records by that attribute.
        """
        df_dates = self.dtype_table.copy()
        df_dates['Pair'] = df_dates.apply(
            lambda x: f"{x['FECHA DE INICIO']}-{x['FECHA DE LLEGADA']}", axis = 1
            )
        pair_groups = df_dates.Pair.unique().tolist()
        df_dates['Group'] = df_dates.Pair.apply(lambda x: pair_groups.index(x) + 1)
        df_dates.drop(['Pair'], axis=1, inplace = True)
        df_dates.rename(columns={'Group': 'Pair'}, inplace = True)
        return df_dates

    def presence_in_db(self) -> pd.DataFrame:
        """
        See the presence of these objects along 
        the columns of start and arrival date to check 
        whether they are in both.
        """ 
        df_dates = self.__pairs_grouping() 
        df_dates = df_dates.melt(id_vars = ['Pair'], 
                                       value_name='Dtype', var_name='Date')
        df_dates.Dtype = df_dates.Dtype.map(str)
        df_dates = df_dates.groupby(
            by = ['Pair', 'Date', 'Dtype']
            ).agg({'Pair': 'count'})
        df_dates.rename(columns={'Pair': 'freq'}, inplace=True) 
        return df_dates