
#############################
#   Imports and Contants    #
#############################

# Python modules

# Local modules
from src.utils_ import timing_decorator, read_json_file_2_dict, create_directory
from src.multi_dimension_design.dimensions.utils_ import FACILITY
from src.multi_dimension_design.dimensions import Date, Table, Location, Hour, Trip_Junk, Vax_Site, Location_Grid
import itertools
import csv
from shapely.wkt import loads

PATH="../data/COVID-19_Vaccinations_by_ZIP_Code.csv"
PATH_vax_sites="../..data/Vax_Sites.csv"

array = []

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

def read_facilities():
    with open('../data/Facilities.csv') as f:
        facilities = []
        for facility_info in f.readlines()[:]:
            facility_info = facility_info.split(',')

            if facility_info[2] == "vax_site":
                facilities.append(facility_info)

        print(facilities)
        return facilities

facilities = read_facilities()

def process_line(line, pipeline_functions,  fact_table):
    sgs = []

    for table, fun in pipeline_functions:
        sg = fun(table, line, sgs)
        if sg == -1:
            return

        sgs.append(str(sg))

    fact_table.write(sgs[-1])


def process_file(filename: str, fact_table, pipeline):
    with open(filename, 'r', encoding = "ISO-8859-1") as f:
        f.readline() # ignore header
        reader = csv.reader(f)

        line = create_header()

        fact_table.write(line)

        for line_number, line in enumerate(reader):
            process_line(line, pipeline, fact_table)


def create_record_data_dimension(table, line, sgs):
    columns = table.header_columns

    idx_id = columns['row_id']
    idx_date = columns['date']
    start_time = line[idx_date]
    original_key = line[idx_id]
    start_date = Date(original_key, start_time, '%m/%d/%Y')
    sg = table.insert(start_date)
    return sg


def aux_location_dimension(table, line):
    columns = table.header_columns

    idx_location = columns['zip_code_location']
    location = line[idx_location]

    try:
        location = loads(location)
    except:
        print("----------------------------" + "rip" + "-----------------------------------")
        return -1, -1;

    temp_coords = [location.x, location.y]
    zip_info = Location.extract_zip_info(zip_codes, temp_coords)

    return temp_coords, zip_info

def create_record_location_dimension(table, line, sgs):
    columns = table.header_columns

    idx_id = columns['row_id']
    original_key = line[idx_id]

    temp_coords, zip_info = aux_location_dimension(table, line)
    try:
        location = Location(original_key, temp_coords, zip_info)
    except:
        print("___________________________________" + "rip" + "___________________________________")
        return - 1;

    sg = table.insert(location)
    return sg


def create_record_location_grid_dimension(table, line, sgs):
    columns = table.header_columns

    idx_id = columns['row_id']
    original_key = line[idx_id]

    temp_coords, zip_info = aux_location_dimension(table, line)
    try:
        location_grid = Location_Grid(original_key, temp_coords, zip_info)
    except:
        print("___________________________________" + "rip" + "___________________________________")
        return - 1;

    sg = table.insert(location_grid)
    return sg

def process_vac(table, line, sgs):
    columns = table

    idx_id = columns['row_id']
    idx_total_doses= columns['total_doses_-_daily']
    idx_1st_doses = columns['1st_dose_-_daily']
    idx_vaccine_series_completed = columns['vaccine_series_completed_-_daily']

    date = sgs[0]

    total_doses = line[idx_total_doses]
    total_doses = str(total_doses).replace(',', '')

    fst_doses = line[idx_1st_doses]
    fst_doses = str(fst_doses).replace(',', '')

    vaccine_series_completed = line[idx_vaccine_series_completed]
    vaccine_series_completed = str(vaccine_series_completed).replace(',', '')

    id_id = line[idx_id]
    location = sgs[1]
   # location_grid = sgs[2]

    if str(id_id).__contains__("Unknown"):
        return

    line = f'{id_id},' \
            f'{date},' \
            f'{total_doses},' \
            f'{fst_doses},' \
            f'{vaccine_series_completed},' \
            f'{location}\n'
            #f'{location_grid}\n'

    array.append(line)
    return line

def write_file(filename, file):
    with open(filename, 'w') as f:
        for line in file:
            f.write(line)

def write_lookup_tables(pipeline):
    for table_info in pipeline:
        table = table_info[0]
        table.write_lookup_table()

def write_tables(pipeline):
    for table,_ in pipeline[:-1]:
        table.write_own_table()

def attrib_id(table, line, counter_curr):
    line[0] = str(counter_curr)
    result = ""
    for piece in line:
        result += piece + ","

    x = result[:-1] + '\n'

    array.append(x)


def create_header():
    line = 'vax_id,' \
           'date,' \
           'total_doses,' \
           'first_doses,' \
           'vaccine_series_completed,' \
           'location\n'
           #'location_grid\n'

    return line

def main():
    tables_info = read_json_file_2_dict("tables_info", "../data")
    headers = tables_info['vaccinations']['columns']

    store_dir = '../../../fact_tables'
    create_directory(store_dir)
    with open('../../../fact_tables/vax_fact.csv', 'w') as f:
        pipeline = [
            (Table(headers, f'data_dimension', 0), create_record_data_dimension),
            (Table(headers, f'location_dimension', 0), create_record_location_dimension),
            #(Table(headers, f'location_grid_dimension', 0), create_record_location_grid_dimension),
            (headers, process_vac)
        ]
        process_file(PATH, f, pipeline)
        write_tables(pipeline)

    write_file("vac_test.csv", array)

    print("FINISH")

if __name__ == '__main__':
    main()