from datetime import datetime
import pandas as pd
import os
os.chdir('/home/carlosfol/My_Documents/Git_Projects/PSI_TRIPS/scripts/trip_management')
from trip_dates import TripDates
from datetimes.trip_duration import TripDuration

class DateTimesObj(TripDates):
    def __init__(self, df_tc):
        super().__init__(df_tc)
        self.df_tc = self.choose_dtypes(dtype_fi=datetime, dtype_fl=datetime)
        
    def filter_by_relationship(self, consistent = True) -> pd.DataFrame:
        """
        Filter the observations by specifying the 
        relationship between the start date and 
        arrival date of the trips
        """
        consistent_cond = self.df_tc.apply(
            lambda x: x['FECHA DE LLEGADA'] >= x['FECHA DE INICIO'],
            axis = 1
        )
        if consistent == True:
            return self.df_tc.loc[consistent_cond, :]
        else:
            return self.df_tc.loc[~consistent_cond, :]
    
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

if __name__ == '__main__':
    df_tc = pd.read_hdf('/home/carlosfol/My_Documents/Git_Projects/PSI_TRIPS/scripts/trip_management/df_tc.h5')
    dt_obj = DateTimesObj(df_tc)
    print(dt_obj.get_correct_arr_date(dt_obj.filter_by_relationship()))