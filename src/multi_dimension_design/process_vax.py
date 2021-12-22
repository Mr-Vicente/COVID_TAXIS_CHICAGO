
#############################
#   Imports and Contants    #
#############################

# Python modules

# Local modules
from src.utils_ import timing_decorator, read_json_file_2_dict
from src.multi_dimension_design.dimensions.utils_ import FACILITY
from src.multi_dimension_design.dimensions import Date, Table, Location, Hour, Trip_Junk, Vax_Site
import itertools
import csv

PATH="../data/COVID-19_Vaccinations_by_ZIP_Code.csv"
PATH_vax_sites="../..data/Vax_Sites.csv"

counter = itertools.count(0)
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

def process_line(line, pipeline_functions):
    for table, fun in pipeline_functions:
        fun(table, line)

def process_file(filename: str, pipeline):
    with open(filename, 'r') as f:
        f.readline() # ignore header
        reader = csv.reader(f)
        for line_number, line in enumerate(reader):
            process_line(line, pipeline)





def process_vac(table, line):
    columns = table

    id = counter.__next__()
    idx_date = columns['date']
    idx_population = columns['population']
    idx_total_doses= columns['total_doses_-_daily']
    idx_1st_doses = columns['1st_dose_-_daily']
    idx_vaccine_series_completed = columns['vaccine_series_completed_-_daily']
    idx_og_id = columns['row_id']

    date = line[idx_date]
    population = line[idx_population]
    total_doses = line[idx_total_doses]
    fst_doses = line[idx_1st_doses]
    vaccine_series_completed = line[idx_vaccine_series_completed]
    og_id = line[idx_og_id]

    if population == "":
        population = "-1"

    population = population.replace(',', '.')

    line = f'{id},' \
           f'{date},' \
           f'{population},' \
           f'{total_doses},' \
           f'{fst_doses},' \
           f'{vaccine_series_completed},' \
           f'{og_id}\n'

    print(line)

    array.append(line)

def write_file(filename, file):
    with open(filename, 'w') as f:
        for line in file:
            f.write(line)

def main():
    tables_info = read_json_file_2_dict("tables_info", "../data")
    headers = tables_info['vaccinations']['columns']


    pipeline = [
        (headers, process_vac)
    ]
    process_file(PATH, pipeline)

    write_file("vac_test.csv", array)

if __name__ == '__main__':
    main()