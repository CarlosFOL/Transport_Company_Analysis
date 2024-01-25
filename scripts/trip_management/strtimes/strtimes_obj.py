import pandas as pd
from ..trip_dates import TripDates

class StrTimes(TripDates):
    
    @property
    def str_table(self) -> pd.DataFrame:
        """
        Table containing the departure and 
        arrival dates of all trips with a str 
        value in any of these columns.
        """
        df_dtypes = self.table.map(type)
        str_dates = df_dtypes.isin([str]).sum(axis=1).map(bool)
        return df_dtypes[str_dates]
    
    @str_table.setter
    def str_table(self, df_tc: pd.DataFrame) -> None:
        """
        Update the content
        """
        self.table = df_tc
    
    def __pairs_grouping(self) -> pd.DataFrame:
        """
        Get the pairs where at least 
        one is a str object. Then, group the 
        records by that attribute.
        """
        df_strdates = self.str_table.copy()
        df_strdates['Pair'] = df_strdates.apply(
            lambda x: f"{x['FECHA DE INICIO']}-{x['FECHA DE LLEGADA']}", axis = 1
            )
        pair_groups = df_strdates.Pair.unique().tolist()
        df_strdates['Group'] = df_strdates.Pair.apply(lambda x: pair_groups.index(x) + 1)
        df_strdates.drop(['Pair'], axis=1, inplace = True)
        df_strdates.rename(columns={'Group': 'Pair'}, inplace = True)
        return df_strdates
    
    def presence_in_db(self) -> pd.DataFrame:
        """
        See the presence of str objects along 
        the columns of start and arrival date to check 
        whether they are in both.
        """ 
        df_strdates = self.__pairs_grouping() 
        df_strdates = df_strdates.melt(id_vars = ['Pair'], 
                                       value_name='Dtype', var_name='Date')
        df_strdates.Dtype = df_strdates.Dtype.map(str)
        df_strdates = df_strdates.groupby(
            by = ['Pair', 'Date', 'Dtype']
            ).agg({'Pair': 'count'})
        df_strdates.rename(columns={'Pair': 'freq'}, inplace=True) 
        return df_strdates