

#############################
#   Imports and Contants    #
#############################

# Python modules

# Local modules
import numpy

from src.utils_ import timing_decorator, read_json_file_2_dict
from src.multi_dimension_design.dimensions import Date, Table, Location,Location_Grid, Hour, Trip_Junk

# Remote modules
import pandas as pd
import bodo
import numpy as np

#PATH="../../../datasets/Full_Covid_Taxi_Trips.csv"
PATH="../../../datasets/2_head_Taxi_Trips.csv"

COLS = [
    'Trip ID',
    'Taxi ID',
    'Trip Start Timestamp',
    'Trip End Timestamp',
    'Trip Seconds',
    'Trip Miles',
    'Fare',
    'Tips',
    'Tolls',
    'Extras',
    'Trip Total',
    'Payment Type',
    'Company',
    'Pickup Centroid Latitude',
    'Pickup Centroid Longitude',
    'Dropoff Centroid Latitude',
    'Dropoff Centroid Longitude'
]

New_Cols = [
    'trip_id',
    'taxi_id',
    'trip_start_timestamp',
    'trip_end_timestamp',
    'trip_seconds',
    'trip_miles',
    'fare',
    'tips',
    'tolls',
    'extras',
    'trip_total',
    'payment_type',
    'company',
    'pickup_centroid_latitude',
    'pickup_centroid_longitude',
    'dropoff_centroid_latitude',
    'dropoff_centroid_longitude'
]


def map_keys(entry, values):
    l = np.where(values==entry)[0].tolist()
    if not l:
        return -1
    else:
        return l[0]

#@bodo.jit(distributed=['dates', 'date_look_up'])
def deal_dates(dates,date_look_up):
    dates['start_time'] = dates['start_timestamp'].apply(lambda time: Date(None, time))
    dates['end_time'] = dates['end_timestamp'].apply(lambda time: Date(None, time))
    dates['start_time_str'] = dates['start_time'].apply(lambda date: str(date))
    dates['end_time_str'] = dates['end_time'].apply(lambda date: str(date))
    dates_ = numpy.concatenate((dates['start_time_str'].values,dates['end_time_str'].values))
    print(dates_)
    unique_dates = numpy.unique(dates_)
    date_look_up['sk_start_time'] = dates['start_time_str'].apply(lambda x: map_keys(x, unique_dates))
    date_look_up['sk_end_time'] = dates['end_time_str'].apply(lambda x: map_keys(x, unique_dates))

def deal_hours(dates,hour_look_up):
    dates['start_hours'] = dates['start_timestamp'].apply(lambda time: Hour(None, time))
    dates['end_hours'] = dates['end_timestamp'].apply(lambda time: Hour(None, time))
    dates['start_hours_str'] = dates['start_hours'].apply(lambda hour: str(hour))
    dates['end_hours_str'] = dates['end_hours'].apply(lambda hour: str(hour))
    hours = numpy.concatenate((dates['start_hours_str'].values,dates['end_hours_str'].values))
    print(hours)
    unique_hours = numpy.unique(hours)
    hour_look_up['sk_start_hours'] = dates['start_hours_str'].apply(lambda x: map_keys(x, unique_hours))
    hour_look_up['sk_end_hours'] = dates['end_hours_str'].apply(lambda x: map_keys(x, unique_hours))

def create_time_dimensions(taxi_table):
    dates = pd.DataFrame(taxi_table[['trip_start_timestamp', 'trip_end_timestamp']])
    dates.columns = ['start_timestamp', 'end_timestamp']
    date_look_up = pd.DataFrame(taxi_table['trip_id'])

    deal_dates(dates, date_look_up)
    print("============")
    hour_look_up = pd.DataFrame(taxi_table['trip_id'])
    deal_hours(dates, hour_look_up)
    print(date_look_up.head(10))
    print(hour_look_up.head(10))

    #create_date_dimension(dates, unique_dates)

#@bodo.jit(distributed=['dates'])
def create_date_dimension(dates, unique_dates):
    pass #date_dimension = pd.DataFrame(taxi_table['trip_id'])


def create_hour_dimension(hours, unique_hours):
    pass



def main():
    tables_info = read_json_file_2_dict("tables_info", "../data")
    headers = tables_info['taxi_trips']['columns']

    taxis = pd.read_csv(PATH, usecols=COLS, sep=',')
    taxis.columns = New_Cols

    print(taxis.head())

    create_time_dimensions(taxis)

if __name__ == '__main__':
    main()