
#############################
#   Imports and Contants    #
#############################

# Python modules

# Local modules
from src.utils import timing_decorator, read_json_file_2_dict
from src.multi_dimension_design.dimensions import Date, Table

PATH="../../../datasets/Full_Covid_Taxi_Trips.csv"

@timing_decorator
def process_line(line, pipeline_functions):
    line = line.split(',')[:-1]
    for table, fun in pipeline_functions:
        fun(table, line)

@timing_decorator
def process_file(filename: str, pipeline):
    x = 0
    with open(filename, 'r') as f:
        f.readline() # ignore header
        for line in f:
            x+=1
            process_line(line, pipeline)
            if x==20:
                break
        print(pipeline[0][0].rows)

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
    pass

def create_location_grid_dimension(table, line):
    pass

def main():
    tables_info = read_json_file_2_dict("tables_info", "../data")
    headers = tables_info['taxi_trips']['columns']
    pipeline = [
        (Table(headers), create_record_data_dimension),
        (Table(headers), create_trip_junk_dimension),
        (Table(headers), create_location_grid_dimension),
    ]
    process_file(PATH, pipeline)

if __name__ == '__main__':
    main()