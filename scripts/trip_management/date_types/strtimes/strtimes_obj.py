import pandas as pd
from ..dtypes import SingleDtype

class StrTimes(SingleDtype):
    
    def __init__(self, df_tc: pd.DataFrame):
        super().__init__(df_tc, str)

    @property
    def str_table(self) -> pd.DataFrame:
        """
        Table containing the departure and 
        arrival dates of all trips with a str 
        value in any of these columns.
        """
        return self.dtype_table
    
    @str_table.setter
    def str_table(self, df_tc: pd.DataFrame) -> None:
        """
        Update the content
        """
        self.table = df_tc