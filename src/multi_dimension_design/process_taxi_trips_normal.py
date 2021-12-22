
#############################
#   Imports and Contants    #
#############################

# Python modules
import csv

# Local modules
from src.utils_ import timing_decorator, read_json_file_2_dict
from src.multi_dimension_design.dimensions import Date, Table, Location,Location_Grid, Hour, Trip_Junk
from utils_ import get_number_of_lines
import sys

#PATH="../../../datasets/Full_Covid_Taxi_Trips.csv"
#PATH="../../../datasets/3_head_Taxi_Trips.csv"
#PATH="../../../datasets/Parsed_Col_Full_Covid_Taxi_Trips.csv"
PATH= "../../../datasets/Shorter_Col_Sorted_Taxi_Trips.csv"


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
def process_line(line_number, line, pipeline_functions, look_up_file):
    sgs = []
    for table, fun in pipeline_functions:
        try:
            sg = fun(table, line)
            sgs.append(str(sg))
        except Exception as _:
            #print("hey: ", line)
            continue
        if line_number % 5000 == 0:
            print(f'{table.name}: {len(list(table.rows_helper.keys()))} rows')
            #print(list(table.lookup_table.items())[:5])
    pk = line[0]
    sgs_str = ','.join(sgs)
    look_up_file.write(f'{pk},{sgs_str}\n')

@timing_decorator
def process_file(filename: str, look_up_file, pipeline, total_lines):
    with open(filename, 'r', encoding = "ISO-8859-1") as f:
        f.readline() # ignore current line
        reader = csv.reader(f)
        for line_number, line in enumerate(reader):
            line_number+=1
            process_line(line_number, line, pipeline, look_up_file)
            if (line_number)%5000 == 0:
                print(f"==============")
                print(f'{line_number}/{total_lines} -> {(line_number/(total_lines))*100}%')
                print(f"==============")
        #print(pipeline[0][0].rows)

def create_record_hour_dimension_start(table, line):
    columns = table.header_columns
    idx_start_time = columns['trip_start_timestamp']
    start_time = line[idx_start_time]
    original_key = line[0]
    start_date = Hour(original_key, start_time)
    sg = table.insert(start_date)
    return sg

def create_record_hour_dimension_end(table, line):
    columns = table.header_columns
    idx_end_time = columns['trip_end_timestamp']
    end_time = line[idx_end_time]
    original_key = line[0]
    end_date = Hour(original_key, end_time)
    sg = table.insert(end_date)
    return sg

def create_record_data_dimension_start(table, line):
    columns = table.header_columns
    idx_start_time = columns['trip_start_timestamp']
    start_time = line[idx_start_time]
    original_key = line[0]
    start_date = Date(original_key, start_time)
    sg = table.insert(start_date)
    return sg

def create_record_data_dimension_end(table, line):
    columns = table.header_columns
    idx_end_time = columns['trip_end_timestamp']
    end_time = line[idx_end_time]
    original_key = line[0]
    end_date = Date(original_key, end_time)
    sg = table.insert(end_date)
    return sg

def create_trip_junk_dimension(table, line):
    columns = table.header_columns
    idx_payment_type = columns['payment_type']
    idx_company = columns['company']
    payment_type = line[idx_payment_type]
    company = line[idx_company]
    original_key = line[0]
    trip_junk = Trip_Junk(original_key, payment_type, company)
    sg = table.insert(trip_junk)
    return sg

def create_location_dimension_start(table, line):
    columns = table.header_columns
    idx_start_latitude = columns['pickup_centroid_latitude']
    idx_start_longitude = columns['pickup_centroid_longitude']
    start_location = [line[idx_start_longitude], line[idx_start_latitude]]
    original_key = line[0]
    start_zip_info = Location.extract_zip_info(zip_codes, start_location)
    start_location = Location_Grid(original_key, start_location, start_zip_info)
    sg = table.insert(start_location)
    return sg

def create_location_dimension_end(table, line):
    columns = table.header_columns
    idx_end_latitude = columns['dropoff_centroid_latitude']
    idx_end_longitude = columns['dropoff_centroid_longitude']
    end_location = [line[idx_end_longitude], line[idx_end_latitude]]
    original_key = line[0]
    end_zip_info = Location.extract_zip_info(zip_codes, end_location)
    end_location = Location_Grid(original_key, end_location, end_zip_info)
    sg = table.insert(end_location)
    return sg

def write_lookup_tables(pipeline):
    for table_info in pipeline:
        table = table_info[0]
        table.write_lookup_table()

def write_tables(pipeline):
    for table,_ in pipeline:
        table.write_own_table()

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

def main():
    set_max_csv()
    tables_info = read_json_file_2_dict("tables_info", "../data")
    headers = tables_info['taxi_trips']['columns']
    total_lines = get_number_of_lines(PATH)
    print(f'Starting processing file with: {total_lines} rows :))')
    with open('../../../lookup_tables/lookup_table.csv', 'w') as f:
        pipeline = [
            (Table(headers, f'data_dimension_start',0),create_record_data_dimension_start),
            (Table(headers, f'data_dimension_end',0), create_record_data_dimension_end),
            (Table(headers, f'hour_dimension_start',0), create_record_hour_dimension_start),
            (Table(headers, f'hour_dimension_end',0), create_record_hour_dimension_end),
            (Table(headers, f'trip_junk_dimension',0), create_trip_junk_dimension),
            (Table(headers, f'location_grid_dimension_start',0), create_location_dimension_start),
            (Table(headers, f'location_grid_dimension_end',0), create_location_dimension_end),
        ]
        process_file(PATH, f, pipeline, total_lines)
        write_tables(pipeline)


if __name__ == '__main__':
    main()