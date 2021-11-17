#############################
#   Imports and Contants    #
#############################

# Python modules

# Local modules
from src.utils import write_dict_2_json_file

def process_file_header(header:str):
    lower_case_header = header.lower()
    new_header = lower_case_header.replace(" ", "_")
    new_columns = new_header.split(",")
    return new_header, new_columns


def read_file_header(filename:str):
    with open(filename, 'r') as f:
        return f.readline()

def process_tables(table_names:[str]):
    tables_info = {}
    for table_name in table_names:
        filename = f"{table_name}"
        header = read_file_header(filename)
        new_header, new_columns = process_file_header(header)
        tables_info[table_name] = {
            "header": new_header,
            "columns": new_columns
        }

    write_dict_2_json_file(json_object=tables_info,filename="tables_info",store_dir="../data")


def main():
    table_names = ["taxi_trips"]
    process_tables(table_names)


if __name__ == '__main__':
    main()