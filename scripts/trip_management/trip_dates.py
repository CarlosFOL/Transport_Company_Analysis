import pandas as pd

class TripDates:
    def __init__(self, df_tc: pd.DataFrame) -> None:
        self.df_tc = df_tc.copy()
    
    @property
    def table(self) -> pd.DataFrame:
        """
        Get the table with the departure 
        and arrival dates of the trips made
        """
        return self.df_tc.loc[:, ['FECHA DE INICIO', 'FECHA DE LLEGADA']].copy()
    
    @table.setter
    def table(self, df_tc: pd.DataFrame) -> None:
        """
        Update the content
        """
        self.df_tc = df_tc
    
    def choose_dtypes(self, dtype_dd: type, dtype_ad: type) -> pd.DataFrame:
        """
        Filter the dates according by 
        the dtypes selected
        """
        dtypes_selected = self.table.apply(
        lambda x: type(x['FECHA DE INICIO']) == dtype_dd
        and type(x['FECHA DE LLEGADA']) == dtype_ad, axis = 1
        )
        return self.table.loc[dtypes_selected, :]