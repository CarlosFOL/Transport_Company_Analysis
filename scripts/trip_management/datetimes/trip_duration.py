from datetime import datetime, time
import pandas as pd

class TripDuration:
    def __init__(self, df_tc: pd.DataFrame):
        self.df_tc = df_tc
    
    def merge_date_and_time(self, df_tc: pd.DataFrame, date_col: str, time_col: str) -> pd.Series:
        """
        Combine the date objetcs with 
        the times objects
        """
        datetimes = df_tc.apply(
        lambda x: datetime.combine(x[date_col], x[time_col]),
        axis = 1 
            )
        return datetimes
    
    def process_times(self, time_column: pd.Series) -> pd.Series:
        """
        Convert in time objects to combine 
        with the dates
        """
        cast_time = lambda x: time(int(x[:2]), int(x[3:5]))
        return time_column.astype(str).apply(cast_time)
    
    def calculate_trip_times(self) -> pd.DataFrame:
        """
        Calculate the trip duration of all 
        the routes traveled
        """
        not_unrgt = ~(self.df_tc.loc[:, ['HORA DE INICIO DEL TRANSITO', 
                                          'HORA DE LLEGADA DESTINO']].isin(
                                              ['Unregistered']
                                            ).any(axis = 1))
        df_td = self.df_tc[not_unrgt].copy()
        df_td['Start_Transit_Time'] = self.process_times(df_td['HORA DE INICIO DEL TRANSITO'])
        df_td['Arrival_Time'] = self.process_times(df_td['HORA DE LLEGADA DESTINO'])
        df_td['Start_Date'] = self.merge_date_and_time(df_td, 'FECHA DE INICIO', 'Start_Transit_Time')
        df_td['Arrival_Date'] = self.merge_date_and_time(df_td, 'FECHA DE LLEGADA', 'Arrival_Time')
        df_td['Route'] = df_td.apply(
            lambda x: f"{x['ORIGEN']} - {x['DESTINO']}",
            axis = 1
        )
        df_td['Trip_Duration'] = df_td.apply(
            lambda x: x['Arrival_Date'] - x['Start_Date'],
            axis = 1
        )
        return df_td.groupby(by = 'Route').agg({'Trip_Duration': 'mean'})