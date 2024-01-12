import pandas as pd

class TripDates:
    def __init__(self, df_tc: pd.DataFrame):
        self.__df_tc = df_tc.copy()
    
    def update_db(self, df_tc: pd.DataFrame) -> None:
        """
        Update database content
        """
        self.__df_tc = df_tc.copy()
    
    def choose_dtypes(self, dtype_fi: object, dtype_fl: object) -> pd.DataFrame:
        """
        Filter the data according by the dtypes 
        selected for the columns FECHA DE INICIO and 
        FECHA DE LLEGADA
        """
        dtypes_selected = self.__df_tc.apply(
        lambda x: type(x['FECHA DE INICIO']) == dtype_fi
        and type(x['FECHA DE LLEGADA']) == dtype_fl, axis = 1
        )
        return self.__df_tc.loc[dtypes_selected, :]