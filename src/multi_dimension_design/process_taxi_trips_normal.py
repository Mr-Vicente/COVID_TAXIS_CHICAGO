
#############################
#   Imports and Contants    #
#############################

# Python modules
import csv

# Local modules
from src.utils_ import timing_decorator, read_json_file_2_dict, create_directory
from src.multi_dimension_design.dimensions import Date, Table, Location,Location_Grid, Hour, Trip_Junk
from utils_ import get_number_of_lines
import sys
import csv

def set_max_csv():
    maxInt = sys.maxsize
    while True:
        # decrease the maxInt value by factor 10
        # as long as the OverflowError occurs.

        try:
            csv.field_size_limit(maxInt)
            break
        except OverflowError:
            maxInt = int(maxInt / 10)

#PATH="../../../datasets/Full_Covid_Taxi_Trips.csv"
#PATH="../../../datasets/3_head_Taxi_Trips.csv"
#PATH="../../../datasets/smoll.csv"
PATH="../../../datasets/Shorter_Col_Cleaner_Sorted_Taxi_Trips.csv"
#PATH="../../../datasets/Parsed_Col_Full_Covid_Taxi_Trips.csv"
#PATH="../../../datasets/Shorter_Sorted_Taxi_Trips.csv"


def read_zip_codes():
    with open('../data/Zip_Codes.csv') as f:
        zip_codes = []
        for zip_info in f.readlines()[1:]:
            zip_info = zip_info.split('"')[1:]
            poligon_vec = zip_info[0]
            att_vec = zip_info[1].split(',')
            poligon = Location.poligon_str_2_poligon(poligon_vec)
            new_zip_info = [poligon] + att_vec
            zip_codes.append(new_zip_info)
        return zip_codes

zip_codes = read_zip_codes()

#@timing_decorator
def process_line(line_number, line, pipeline_functions, taxi_fact_table, taxi_grid_fact_table):
    sgs = []
    for table, fun in pipeline_functions:

        sg = fun(table, line, sgs)
        if sg[0] == -1:
            return

        sgs.append(str(sg[0]))
        if len(sg) > 1:
            sgs.append(str(sg[1]))

       # if line_number % 5000 == 0:
            #print(f'{table.name}: {len(list(table.rows_helper.keys()))} rows')
            #print(list(table.lookup_table.items())[:5])
    pk = line[0]
    sgs_str = ','.join(sgs)

    taxi_fact_table.write(sgs[-2])
    taxi_grid_fact_table.write(sgs[-1])

@timing_decorator
def process_file(filename: str, taxi_fact_table, taxi_grid_fact_table, pipeline, total_lines):
    with open(filename, 'r', encoding = "ISO-8859-1") as f:
        f.readline() # ignore current line
        reader = csv.reader(f)

        line, line_grid = create_header()
        taxi_fact_table.write(line)
        taxi_grid_fact_table.write(line_grid)

        for line_number, line in enumerate(reader):
            line_number+=1
            process_line(line_number, line, pipeline, taxi_fact_table, taxi_grid_fact_table)
            if (line_number)%5000 == 0:
                print(f"==============")
                print(f'{line_number}/{total_lines} -> {(line_number/(total_lines))*100}%')
                print(f"==============")
        #print(pipeline[0][0].rows)

def create_record_hour_dimension_start(table, line, sgs):
    columns = table.header_columns
    idx_start_time = columns['trip_start_timestamp']
    start_time = line[idx_start_time]
    original_key = line[0]
    start_date = Hour(original_key, start_time)
    sg = table.insert(start_date)

    idx_end_time = columns['trip_end_timestamp']
    end_time = line[idx_end_time]
    end_date = Hour(original_key, end_time)
    sg2 = table.insert(end_date)

    return [sg, sg2]

def create_record_data_dimension_start(table, line, sgs):
    columns = table.header_columns
    idx_start_time = columns['trip_start_timestamp']
    start_time = line[idx_start_time]
    original_key = line[0]
    start_date = Date(original_key, start_time)
    sg = table.insert(start_date)

    idx_end_time = columns['trip_end_timestamp']
    end_time = line[idx_end_time]
    end_date = Date(original_key, end_time)
    sg2 = table.insert(end_date)

    return [sg, sg2]

def create_trip_junk_dimension(table, line, sgs):
    columns = table.header_columns
    idx_payment_type = columns['payment_type']
    idx_company = columns['company']
    payment_type = line[idx_payment_type]
    company = line[idx_company]
    original_key = line[0]
    trip_junk = Trip_Junk(original_key, payment_type, company)
    sg = table.insert(trip_junk)
    return [sg]


def aux_location_dimension(table, line):
    columns = table.header_columns
    idx_start_latitude = columns['pickup_centroid_latitude']
    idx_start_longitude = columns['pickup_centroid_longitude']
    start_location = [line[idx_start_longitude], line[idx_start_latitude]]
    start_zip_info = Location.extract_zip_info(zip_codes, start_location)

    idx_end_latitude = columns['dropoff_centroid_latitude']
    idx_end_longitude = columns['dropoff_centroid_longitude']
    end_location = [line[idx_end_longitude], line[idx_end_latitude]]
    end_zip_info = Location.extract_zip_info(zip_codes, end_location)

    return start_location, end_location, start_zip_info, end_zip_info;


def create_location_dimension_start(table, line, sgs):
    start_location, end_location, start_zip_info, end_zip_info = aux_location_dimension(table, line)
    original_key = line[0]

    try:
        start_location = Location(original_key, start_location, start_zip_info)
        end_location = Location(original_key, end_location, end_zip_info)
    except:
        print("---------Broken---------")
        return [-1];

    sg = table.insert(start_location)
    sg2 = table.insert(end_location)
    return [sg, sg2]


def create_location_grid_dimension_start(table, line, sgs):
    start_location, end_location, start_zip_info, end_zip_info = aux_location_dimension(table, line)
    original_key = line[0]

    try:
        start_location = Location_Grid(original_key, start_location, start_zip_info)
        end_location = Location_Grid(original_key, end_location, end_zip_info)
    except:
        print("---------Broken---------")
        return [-1];

    sg = table.insert(start_location)
    sg2 = table.insert(end_location)
    return [sg, sg2]


def process_trip(table, line, sgs):
    columns = table
    idx_trip_id = columns['trip_id']
    idx_taxi_id = columns['taxi_id']

    idx_trip_seconds = columns['trip_seconds']
    idx_trip_miles = columns['trip_miles']
    idx_trip_fare = columns['fare']
    idx_trip_tips = columns['tips']
    idx_trip_tolls = columns['tolls']
    idx_trip_extras = columns['extras']
    idx_trip_total = columns['trip_total']
    idx_start_latitude = columns['pickup_centroid_latitude']
    idx_start_longitude = columns['pickup_centroid_longitude']
    idx_end_latitude = columns['dropoff_centroid_latitude']
    idx_end_longitude = columns['dropoff_centroid_longitude']

    trip_id = line[idx_trip_id]
    taxi_id = line[idx_taxi_id]
    trip_seconds = line[idx_trip_seconds]
    trip_miles = line[idx_trip_miles]
    trip_fare = line[idx_trip_fare]
    trip_tips = line[idx_trip_tips]
    trip_tolls = line[idx_trip_tolls]
    trip_extras = line[idx_trip_extras]
    trip_total = line[idx_trip_total]
    trip_start_latitude = line[idx_start_latitude]
    trip_start_longitude = line[idx_start_longitude]
    trip_end_latitude = line[idx_end_latitude]
    trip_end_longitude = line[idx_end_longitude]

    trip_date_start = sgs[0]
    trip_date_ends = sgs[1]
    trip_start_hour = sgs[2]
    trip_end_hour = sgs[3]
    trip_junk = sgs[4]
    trip_location_grid_start = sgs[5]
    trip_location_grid_end = sgs[6]

    line = f'{trip_id},' \
            f'{taxi_id},' \
            f'{trip_seconds},' \
            f'{trip_miles},' \
            f'{trip_fare},' \
            f'{trip_tips},' \
            f'{trip_tolls},' \
            f'{trip_extras},' \
            f'{trip_total},' \
            f'{trip_start_hour},' \
            f'{trip_end_hour},' \
            f'{trip_date_start},' \
            f'{trip_date_ends},' \
            f'{trip_junk},' \
            f'{trip_start_latitude},' \
            f'{trip_start_longitude},' \
            f'{trip_end_latitude},' \
            f'{trip_end_longitude}\n'

    line_grid = f'{trip_id},' \
                f'{taxi_id},' \
                f'{trip_seconds},' \
                f'{trip_miles},' \
                f'{trip_fare},' \
                f'{trip_tips},' \
                f'{trip_tolls},' \
                f'{trip_extras},' \
                f'{trip_total},' \
                f'{trip_start_hour},' \
                f'{trip_end_hour},' \
                f'{trip_date_start},' \
                f'{trip_date_ends},' \
                f'{trip_junk},' \
                f'{trip_location_grid_start},' \
                f'{trip_location_grid_end}\n'


   # print(line)
    return [line, line_grid]


def create_header():
    line =  'trip_id,' \
            'taxi_id,' \
            'trip_seconds,' \
            'trip_miles,' \
            'trip_fare,' \
            'trip_tips,' \
            'trip_tolls,' \
            'trip_extras,' \
            'trip_total,' \
            'trip_start_hour,' \
            'trip_end_hour,' \
            'trip_date_start,' \
            'trip_date_ends,' \
            'trip_junk,' \
            'pickup_centroid_latitude,' \
            'pickup_centroid_longitude,' \
            'dropoff_centroid_latitude,' \
            'dropoff_centroid_longitude\n'

    line_grid = 'trip_id,' \
                'taxi_id,' \
                'trip_seconds,' \
                'trip_miles,' \
                'trip_fare,' \
                'trip_tips,' \
                'trip_tolls,' \
                'trip_extras,' \
                'trip_total,' \
                'trip_start_hour,' \
                'trip_end_hour,' \
                'trip_date_start,' \
                'trip_date_ends,' \
                'trip_junk,' \
                'trip_location_grid_start,' \
                'trip_location_grid_end\n'
    return line, line_grid

def write_lookup_tables(pipeline):
    for table_info in pipeline:
        table = table_info[0]
        table.write_lookup_table()

def write_tables(pipeline):
    for table,_ in pipeline[:-1]:
        table.write_own_table()


use_location_grid = False


def main():
    global use_location_grid
    set_max_csv()

    tables_info = read_json_file_2_dict("tables_info", "../data")
    headers = tables_info['taxi_trips']['columns']
    total_lines = get_number_of_lines(PATH)
    print(f'Starting processing file with: {total_lines} rows :))')

    store_dir = '../../../fact_tables'
    create_directory(store_dir)
    # self.f = open(f'{store_dir}/{name}.csv', 'w')

    with open('../../../fact_tables/Taxi_fact.csv', 'w') as f:
        with open('../../../fact_tables/Taxi_Grid_fact.csv', 'w') as ff:
            pipeline = [
                (Table(headers, f'data_dimension_start',0),create_record_data_dimension_start),
                (Table(headers, f'hour_dimension_start',0), create_record_hour_dimension_start),
                (Table(headers, f'trip_junk_dimension',0), create_trip_junk_dimension),
                (Table(headers, f'location_grid_dimension_start',0), create_location_grid_dimension_start),

                (headers, process_trip)
            ]
            process_file(PATH, f, ff, pipeline, total_lines)
            write_tables(pipeline)



if __name__ == '__main__':
    main()