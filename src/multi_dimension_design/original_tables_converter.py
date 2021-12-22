#############################
#   Imports and Contants    #
#############################

# Python modules
import re
# Local modules
from src.utils_ import write_dict_2_json_file

def process_file_header(header:str):
    original_header = header
    lower_case_header = header.lower()[:-1]
    new_header = re.sub('\s+', '_', lower_case_header)
    new_columns = new_header.split(",")
    new_columns = {value:i for i,value in enumerate(new_columns)}
    return original_header, new_header, new_columns


def retrieve_first_2_lines(filename:str):
    with open(filename, 'r') as f:
        return f.readline(), f.readline()

def process_tables(table_names:[(str,str)]):
    tables_info = {}
    for table_name, filename in table_names:
        print(table_name, filename)
        header, sample_line = retrieve_first_2_lines(filename)
        original_header, new_header, new_columns = process_file_header(header)
        tables_info[table_name] = {
            "original_header": original_header,
            "header": new_header,
            "sample": sample_line,
            "columns": new_columns
        }
    filename = f'tables_info'
    output_dir = "../data"
    write_dict_2_json_file(json_object=tables_info,filename=filename,store_dir=output_dir)


def main():
    table_names = [
        #("taxi_trips", "../../../datasets/Parsed_Col_Full_Covid_Taxi_Trips.csv"),
        #("taxi_trips", "../../../datasets/Full_Covid_Taxi_Trips.csv"),
        ("taxi_trips", "../../../datasets/Shorter_Col_Sorted_Taxi_Trips.csv"),
        ("vaccinations", "../data/COVID-19_Vaccinations_by_ZIP_Code.csv"),
        ("clinics", "../data/Clinics.csv"),
        ("hospitals", "../data/Hospitals.csv"),
        ("test_sites", "../data/Test_Sites.csv"),
        ("vax_sites", "../data/Vax_Sites.csv"),

    ]
    process_tables(table_names)


if __name__ == '__main__':
    main()