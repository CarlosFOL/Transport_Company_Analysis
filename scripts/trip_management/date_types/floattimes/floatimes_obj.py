import pandas as pd
from ..dtypes import SingleDtype

class FloatTimes(SingleDtype):
    def __init__(self, df_tc: pd.DataFrame):
        super().__init__(df_tc, float)
        
    @property
    def float_table(self) -> pd.DataFrame:
        """
        Table containing the departure and 
        arrival dates of all trips with a float 
        value in any of these columns.
        """
        return self.dtype_table
    
    @float_table.setter
    def float_table(self, df_tc: pd.DataFrame) -> None:
        """
        Update the content
        """
        self.table = df_tc