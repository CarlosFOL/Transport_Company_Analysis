from datetime import datetime, time
from .datetimes_obj import DatetimesObj
import pandas as pd

class TripDuration(DatetimesObj):
    def __init__(self, df_tc: pd.DataFrame):
        super().__init__(df_tc)
        self.df_tc = self.filter_by_relationship()
    
    def __merge_date_and_time(self, df_tc: pd.DataFrame, date_col: str, time_col: str) -> pd.Series:
        """
        Combine the date objetcs with 
        the times objects
        """
        datetimes = df_tc.apply(
        lambda x: datetime.combine(x[date_col], x[time_col]),
        axis = 1 
            )
        return datetimes
    
    def __process_times(self, time_column: pd.Series) -> pd.Series:
        """
        Convert in time objects to combine 
        with the dates
        """
        cast_time = lambda x: time(int(x[:2]), int(x[3:5]))
        return time_column.astype(str).apply(cast_time)
    
    @property
    def table_trip_durations(self) -> pd.DataFrame:
        """
        Table with the trip duration 
        of all the routes traveled
        """
        not_unrgt = ~(self.df_tc.loc[:, ['HORA DE INICIO DEL TRANSITO', 
                                          'HORA DE LLEGADA DESTINO']].isin(
                                              ['Unregistered']
                                            ).any(axis = 1))
        df_td = self.df_tc[not_unrgt].copy()
        df_td['Start_Transit_Time'] = self.__process_times(df_td['HORA DE INICIO DEL TRANSITO'])
        df_td['Arrival_Time'] = self.__process_times(df_td['HORA DE LLEGADA DESTINO'])
        df_td['Start_Date'] = self.__merge_date_and_time(df_td, 'FECHA DE INICIO', 'Start_Transit_Time')
        df_td['Arrival_Date'] = self.__merge_date_and_time(df_td, 'FECHA DE LLEGADA', 'Arrival_Time')
        df_td['Route'] = df_td.apply(
            lambda x: f"{x['ORIGEN']} - {x['DESTINO']}",
            axis = 1
        )
        df_td['Trip_Duration'] = df_td.apply(
            lambda x: x['Arrival_Date'] - x['Start_Date'],
            axis = 1
        )
        return df_td.groupby(by = 'Route').agg({'Trip_Duration': 'mean'})
    
    def __find_trip_duration(self, df_trips: pd.DataFrame) -> pd.DataFrame:
        """
        Find the trip duration of 
        specific routes
        """
        routes = df_trips.apply(lambda x: f"{x['ORIGEN']} - {x['DESTINO']}", axis = 1)
        routes.name = 'Routes'
        trip_durations = pd.merge(
            left = self.table_trip_durations, right = routes, 
            left_index = True, right_on='Routes'
            )     
        return trip_durations.iloc[:, [1, 0]]
    
    def get_correct_arr_date(self, df_trips: pd.DataFrame) -> pd.Series:
        """
        Get the correct arrival dates by adding 
        the departure dates with the trip durations
        """
        routes_duration = self.__find_trip_duration(df_trips)['Trip_Duration']
        arrival_dates = (
            pd.to_datetime(df_trips['FECHA DE INICIO']) +
            pd.to_timedelta(df_trips['HORA DE INICIO DEL TRANSITO'].astype(str)) +
            pd.to_timedelta(routes_duration)
            )
        return arrival_dates