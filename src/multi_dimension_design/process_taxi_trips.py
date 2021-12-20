
#############################
#   Imports and Contants    #
#############################

# Python modules
import csv
import threading
import multiprocessing

# Local modules
from src.utils_ import timing_decorator, read_json_file_2_dict
from src.multi_dimension_design.dimensions import Date, Table, Location,Location_Grid, Hour, Trip_Junk
from utils_ import get_number_of_lines

#PATH="../../../datasets/Full_Covid_Taxi_Trips.csv"
PATH="../../../datasets/3_head_Taxi_Trips.csv"
import os

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
            #print(zip_codes[0])
        return zip_codes

zip_codes = read_zip_codes()

#@timing_decorator
def process_line(line_number, line, pipeline_functions):
    #line = line.split(',')[:-1]
    for table, fun in pipeline_functions:
        try:
            fun(table, line)
        except Exception as _:
            #print("hey: ", line)
            continue
        if line_number % 5000 == 0:
            print(f'{table.name}: {len(table.rows)} rows')
            #print(list(table.lookup_table.items())[:5])

@timing_decorator
def process_file(filename: str, id, offset, upperbound, pipeline):
    upperbound = upperbound-1
    with open(filename, 'r') as f:
        f.seek(offset)
        f.readline() # ignore current line
        reader = csv.reader(f)
        #f.readline() # ignore header
        file_pos = f.tell()
        for line_number, line in enumerate(reader):
            #if '2019' in line or '2021' in line:
            #    continue
            #if line_number < offset:
            #    continue
            #line_number += offset
            file_pos += len(line)
            if file_pos >= upperbound:
                break
            process_line(line_number, line, pipeline)
            if (line_number)%5000 == 0:
                print(f"=======Thread {id}=======")
                print("Line Number: ", line_number)
                print(f'{line_number}/{upperbound-offset} -> {(line_number/(upperbound-offset))*100}%')
                print(f"=================")
        #print(pipeline[0][0].rows)

def create_record_hour_dimension(table, line):
    columns = table.header_columns
    idx_start_time = columns['trip_start_timestamp']
    idx_end_time = columns['trip_end_timestamp']
    start_time = line[idx_start_time]
    end_time = line[idx_end_time]
    original_key = line[0]
    start_date = Hour(original_key, start_time)
    end_date = Hour(original_key, end_time)
    table.insert(start_date)
    table.insert(end_date)

def create_record_data_dimension(table, line):
    columns = table.header_columns
    idx_start_time = columns['trip_start_timestamp']
    idx_end_time = columns['trip_end_timestamp']
    start_time = line[idx_start_time]
    end_time = line[idx_end_time]
    original_key = line[0]
    start_date = Date(original_key, start_time)
    end_date = Date(original_key, end_time)
    table.insert(start_date)
    table.insert(end_date)

def create_trip_junk_dimension(table, line):
    columns = table.header_columns
    idx_payment_type = columns['payment_type']
    idx_company = columns['company']
    payment_type = line[idx_payment_type]
    company = line[idx_company]
    original_key = line[0]
    trip_junk = Trip_Junk(original_key, payment_type, company)
    table.insert(trip_junk)

def create_location_dimension(table, line):
    columns = table.header_columns
    idx_start_latitude = columns['pickup_centroid_latitude']
    idx_start_longitude = columns['pickup_centroid_longitude']
    idx_end_latitude = columns['dropoff_centroid_latitude']
    idx_end_longitude = columns['dropoff_centroid_longitude']
    start_location = [line[idx_start_longitude], line[idx_start_latitude]]
    end_location = [line[idx_end_longitude], line[idx_end_latitude]]
    original_key = line[0]
    start_zip_info = Location.extract_zip_info(zip_codes, start_location)
    end_zip_info = Location.extract_zip_info(zip_codes, end_location)
    if start_zip_info == "" or end_zip_info == "":
        return
    start_location = Location_Grid(original_key, start_location, start_zip_info)
    end_location = Location_Grid(original_key, end_location, end_zip_info)
    table.insert(start_location)
    table.insert(end_location)

def write_lookup_tables(pipeline):
    for table_info in pipeline:
        table = table_info[0]
        table.write_lookup_table()

def write_tables(pipeline):
    for table,_ in pipeline:
        table.write_table()

class Taxi_Thread (threading.Thread):
    def __init__(self, threadID, offset,upper_bound, pipeline):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.offset = offset #if offset != 0 else 1
        self.upper_bound = upper_bound
        self.pipeline = pipeline

    def run(self):
        process_file(PATH, self.threadID,  self.offset, self.upper_bound, self.pipeline)

def main():
    tables_info = read_json_file_2_dict("tables_info", "../data")
    headers = tables_info['taxi_trips']['columns']
    threads = []
    n_threads = 1#multiprocessing.cpu_count()
    print(f'Number of threads: {n_threads} :))')
    total_lines = 20383376#get_number_of_lines(PATH)
    total_bytes = os.path.getsize(PATH)
    print(f'Starting processing file with: {total_bytes} bytes :))')
    print(f'Starting processing file with: {total_lines} rows :))')
    CHUNK_SIZE  = total_bytes // n_threads
    for i in range(n_threads):
        offset = 5000*i
        pipeline = [
            (Table(headers, f'data_dimension_{i}', offset), create_record_data_dimension),
            (Table(headers, f'hour_dimension_{i}', offset), create_record_hour_dimension),
            (Table(headers, f'trip_junk_dimension_{i}', offset), create_trip_junk_dimension),
            (Table(headers, f'location_grid_dimension_{i}', offset), create_location_dimension),
        ]
        offset = i * CHUNK_SIZE
        upper_bound = (i + 1) * CHUNK_SIZE
        thread = Taxi_Thread(i, offset,upper_bound, pipeline)
        thread.start()
        threads.append(thread)
    for t in threads:
        t.join()
    #write_lookup_tables(pipeline)
    #write_tables(pipeline)

    n_dimensions = 4
    for i_dimension in range(n_dimensions):
        tables = []
        for t in threads:
            table = t.pipeline[i_dimension][0]
            tables.append(table)
        look = Table.merge_tables(tables)
        #print(i_dimension , look)


if __name__ == '__main__':
    main()