
#############################
#   Imports and Contants    #
#############################

# Python modules

# Local modules
from src.utils import timing_decorator, read_json_file_2_dict
from src.multi_dimension_design.dimensions import Date, Table, Location, Hour, Trip_Junk

PATH="../..data/COVID-19_Vaccinations_by_ZIP_Code.csv"

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
            if '2019' in line or '2021' in line:
                continue
            x+=1
            process_line(line, pipeline)
            if x==2000:
                break
        print(pipeline[0][0].rows)

def create_record_facicity_dimension(table, line):
    columns = table.header_columns
    idx_start_time = columns['trip_start_timestamp']
    idx_end_time = columns['trip_end_timestamp']
    start_time = line[idx_start_time]
    end_time = line[idx_end_time]
    original_key = line[0]
    start_date = Date(original_key, start_time)
    end_date = Date(original_key, end_time)
    #facility = Facility(...)
    #table.insert(facility)

def write_lookup_tables(pipeline):
    for table_info in pipeline:
        table = table_info[0]
        table.write_lookup_table()

def main():
    tables_info = read_json_file_2_dict("tables_info", "../data")
    headers = tables_info['vaccinations']['columns']
    pipeline = [
        (Table(headers, 'facility_dimension'), create_record_facicity_dimension),
        #(Table(headers), create_record_hour_dimension),
        #(Table(headers), create_trip_junk_dimension),
        #(Table(headers), create_location_dimension),
    ]
    process_file(PATH, pipeline)
    write_lookup_tables(pipeline)

if __name__ == '__main__':
    main()