from datetime import datetime
import pandas as pd
from ..dtypes import DateTypes
# from .trip_duration import TripDuration

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
    
    # @property
    # def trip_duration(self) -> pd.DataFrame:
    #     """
    #     Get the table with the average 
    #     trip duration of all the routes
    #     """
    #     df_trip_duration = TripDuration(self.filter_by_relationship())
    #     return df_trip_duration.calculate_trip_times()
    
    # def find_trip_duration(self, df_trips: pd.DataFrame) -> pd.DataFrame:
    #     """
    #     Find the trip duration of 
    #     specific routes
    #     """
    #     routes = df_trips.apply(lambda x: f"{x['ORIGEN']} - {x['DESTINO']}", axis = 1)
    #     routes.name = 'Routes'
    #     trip_durations = pd.merge(
    #         left = self.trip_duration, right = routes, 
    #         left_index = True, right_on='Routes'
    #         )     
    #     return trip_durations.iloc[:, [1, 0]]
    
    # def get_correct_arr_date(self, df_trips: pd.DataFrame) -> pd.Series:
    #     """
    #     Get the correct arrival dates by adding 
    #     the departure dates with the trip durations
    #     """
    #     routes_duration = self.find_trip_duration(df_trips)['Trip_Duration']
    #     arrival_dates = (
    #         pd.to_datetime(
    #             self.dt_table.loc[routes_duration.index, 'FECHA DE INICIO']
    #             ) + pd.to_timedelta(
    #             routes_duration
    #             )
    #         )
    #     return arrival_dates