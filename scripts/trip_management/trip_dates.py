from datetime import datetime
import pandas as pd
from .trip_duration import TripDuration

class TripDates:
    def __init__(self, df_tc: pd.DataFrame):
        self.df_tc = df_tc
    
    def get_datetimes_obj(self, consistent = True) -> pd.DataFrame:
        """
        Get the trips that have datetimes objects in the
        Arrival and Start Date column and filter them by
        checking whether the condition is accomplished:
        Arrival Date >= Start Date
        """
        datetime_obj = self.df_tc.apply(
        lambda x: type(x['FECHA DE INICIO']) == datetime
        and type(x['FECHA DE LLEGADA']) == datetime, axis = 1
        )
        df_datetime_obj = self.df_tc.loc[datetime_obj, :]
        consistent_cond = df_datetime_obj.apply(
            lambda x: x['FECHA DE LLEGADA'] >= x['FECHA DE INICIO'],
            axis = 1
        )
        if consistent == True:
            return df_datetime_obj.loc[consistent_cond, :]
        else:
            return df_datetime_obj.loc[~consistent_cond, :]
    
    def get_trip_duration(self) -> pd.DataFrame:
        """
        Get the table with the average 
        trip duration of all the routes
        """
        df_trip_duration = TripDuration(self.get_datetimes_obj())
        return df_trip_duration.calculate_trip_times()
    
    def find_trip_duration(self, df_trips: pd.DataFrame) -> pd.DataFrame:
        """
        Find the trip duration of 
        specific routes
        """
        routes = df_trips.apply(lambda x: f"{x['ORIGEN']} - {x['DESTINO']}", axis = 1)
        routes.name = 'Routes'
        df_trip_duration = self.get_trip_duration()
        trip_duration = pd.merge(
            left = df_trip_duration, right = routes, 
            left_index = True, right_on='Routes'
            )     
        return trip_duration.iloc[:, [1, 0]]
    
    def get_correct_arr_date(self, df_trips: pd.DataFrame):
        """
        Get the correct arrival dates by adding 
        the start dates and the trip durations
        """
        routes_duration = self.find_trip_duration(df_trips)
        arrival_dates = (
            pd.to_datetime(
                self.df_tc.loc[routes_duration.index, 'FECHA DE INICIO']
                ) + pd.to_timedelta(
                routes_duration['Trip_Duration']
                )
            )
        return arrival_dates
        