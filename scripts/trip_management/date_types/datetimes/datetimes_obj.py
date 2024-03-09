from datetime import datetime
import pandas as pd
from ..dtypes import DateTypes

class DatetimesObj(DateTypes):
    
    @property
    def dt_table(self) -> pd.DataFrame:
        """
        Get the table with departure and arrival 
        dates whose dtype is datetime
        """
        table = pd.merge(
            left=self.customized_dtypes(dtype_dd=datetime, dtype_ad=datetime),
            right = self.df_tc.loc[:, ['FECHA', 'FECHA TRANSFERENCIA',
                                       'HORA DE INICIO DEL TRANSITO', 'DESTINO',
                                       'HORA DE LLEGADA DESTINO', 'ORIGEN']],
            left_index= True,
            right_index = True
            )
        return table
    
    @dt_table.setter
    def dt_table(self, df_tc: pd.DataFrame) -> None:
        """
        Update the content
        """
        self.table = df_tc
    
    def filter_by_relationship(self, consistent = True) -> pd.DataFrame:
        """
        Filter the observations by checking 
        whether departure date < arrival date
        """
        consistent_cond = self.dt_table.apply(
            lambda x: x['FECHA DE LLEGADA'] >= x['FECHA DE INICIO'],
            axis = 1
        )
        if consistent == True:
            return self.dt_table.loc[consistent_cond, :]
        else:
            return self.dt_table.loc[~consistent_cond, :]