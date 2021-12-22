
#############################
#   Imports and Contants    #
#############################

# Python modules

# Local modules
from shapely.wkt import loads
import csv
from src.utils_ import read_json_file_2_dict
from src.multi_dimension_design.dimensions.utils_ import FACILITY
from src.multi_dimension_design.dimensions import Date, Table, Hour, Trip_Junk, Facility
import itertools

PATH_clinics = "../data/Clinics.csv"
PATH_hospitals = "../data/Hospitals.csv"
PATH_test_sites = "../data/Test_Sites.csv"
PATH_vax_sites = "../data/Vax_Sites.csv"


def process_file(filename, file, idx, facility_type, counter, delimiter):
    with open(filename, 'r') as f:
        f.readline()
        reader = csv.reader(f, delimiter=delimiter)
        for line_number, line in enumerate(reader):

            original_key = counter.__next__()

            print(line)
            print(len(line))

            name = line[idx[0]]
            location = line[idx[1]]


            try:
                location = loads(location)
            except:
                print("----------------------------" + name + "-----------------------------------")

            facility = Facility(original_key, name, facility_type, location)
            #print(str(facility))
            file.append(facility)


def write_file(filename, file):
    with open(filename, 'w') as f:
        for line in file:
            f.write(str(line) + '\n')


def main():
    tables_info = read_json_file_2_dict("tables_info", "../data")
    headers_clinics = tables_info['clinics']['columns']
    headers_hospitals = tables_info['hospitals']['columns']
    headers_test_sites = tables_info['test_sites']['columns']
    headers_vax_sites = tables_info['vax_sites']['columns']

    counter = itertools.count(0)
    file = []

    idx = [headers_clinics["site_name"], headers_clinics["location"]]
    process_file(PATH_clinics, file, idx, FACILITY.CLINIC, counter, ',')

    idx = [headers_hospitals["facility"], headers_hospitals["location"]]
    process_file(PATH_hospitals, file, idx, FACILITY.HOSPITAL, counter, ';')

    idx = [headers_test_sites["facility"], headers_test_sites["location"]]
    process_file(PATH_test_sites, file, idx, FACILITY.TEST_SITE, counter, ',')

    idx = [headers_vax_sites["facility_name"], headers_vax_sites["location"]]
    process_file(PATH_vax_sites, file, idx, FACILITY.VAX_SITE, counter, ',')

    write_file("test.csv", file)
    print("Finish")


if __name__ == '__main__':
    main()