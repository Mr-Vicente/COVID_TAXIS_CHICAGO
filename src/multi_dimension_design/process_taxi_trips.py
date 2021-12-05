
#############################
#   Imports and Contants    #
#############################

# Python modules

# Local modules
from src.utils import timing_decorator, read_json_file_2_dict
from src.multi_dimension_design.dimensions import Date, Table, Location, Hour

PATH="../../../datasets/Full_Covid_Taxi_Trips.csv"

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
            print(zip_codes[0])
        return zip_codes

zip_codes = read_zip_codes()

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
    pass

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
    start_location = Location(original_key, start_location, start_zip_info)
    end_location = Location(original_key, end_location, end_zip_info)
    table.insert(start_location)
    table.insert(end_location)


def main():
    tables_info = read_json_file_2_dict("tables_info", "../data")
    headers = tables_info['taxi_trips']['columns']
    pipeline = [
        #(Table(headers), create_record_data_dimension),
        #(Table(headers), create_record_hour_dimension),
        #(Table(headers), create_trip_junk_dimension),
        (Table(headers), create_location_dimension),
    ]
    process_file(PATH, pipeline)

if __name__ == '__main__':
    main()