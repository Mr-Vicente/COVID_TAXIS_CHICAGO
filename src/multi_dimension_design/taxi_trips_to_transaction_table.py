
#############################
#   Imports and Contants    #
#############################

# Python modules

# Local modules
from src.utils_ import timing_decorator, read_json_file_2_dict
from utils_ import load_lookup_table, get_number_of_lines
from src.multi_dimension_design.dimensions import Date, Table, Location, Hour, Trip_Junk

PATH="../../../datasets/Full_Covid_Taxi_Trips.csv"

def look_up_2(lookup_table, id_):
    for key, value in lookup_table.items():
        if id_ in value:
            return key

def look_up(lookup_table, id_):
    key = lookup_table.get(str(id_), -1)
    assert key != -1
    return key

@timing_decorator
def process_line(line, table, lookup_tables):
    line = line.split(',')[:-1]
    columns = table.header_columns
    idx_trip_seconds = columns['trip_seconds']
    idx_miles = columns['trip_miles']
    idx_fare = columns['trip_fare']
    idx_tips = columns['trip_tips']
    idx_tolls = columns['trip_tolls']
    idx_extras = columns['trip_extras']
    idx_trip_total = columns['trip_trip_total']
    idx_payment_type = columns['trip_payment_type']
    idx_company = columns['trip_company']
    original_key = line[0]
    key_location_start = look_up(lookup_tables[0], original_key)
    key_location_end = look_up(lookup_tables[1], original_key)
    pk = table._next()
    new_line = f'{pk},' \
               f'{line[idx_trip_seconds]},' \
               f'{line[idx_miles]},' \
               f'{line[idx_fare]},' \
               f'{line[idx_tips]},' \
               f'{line[idx_tolls]},' \
               f'{line[idx_extras]},' \
               f'{line[idx_trip_total]},' \
               f'{line[idx_payment_type]},' \
               f'{line[idx_company]},' \
               f'{line[key_location_start]},' \
               f'{line[key_location_end]}\n'
    return new_line

@timing_decorator
def process_trips_agglomerate(filename: str, table, lookup_tables):
    total_lines = get_number_of_lines(filename)
    print(f'Starting processing file with: {total_lines} rows :))')
    new_header = ['id',
                  'trip_seconds',
                  'trip_miles',
                  'trip_tips',
                  'trip_tolls',
                  'trip_extras',
                  'trip_trip_total',
                  'trip_payment_type',
                  'trip_company',
                  'key_location_start',
                  'key_location_end'
                  ]
    new_header_str = f"{','.join(new_header)}\n"
    with open(filename, 'r') as f:
        with open(f'new_{filename}', 'w') as nf:
            f.readline() # ignore header
            nf.write(new_header_str)
            for line_number, line in enumerate(f):
                line_number+=1
                new_line = process_line(line, table, lookup_tables)
                nf.write(new_line)
                if line_number % 5000 == 0:
                    print(f'{line_number}/{total_lines} -> {(line_number / total_lines) * 100}%')

def main():
    tables_info = read_json_file_2_dict("tables_info", "../data")
    headers = tables_info['taxi_trips']['columns']
    look_up_tables_names = ['location_dimension']
    table = Table(headers, 'Chicago_Taxi_Trips_Zones')
    look_up_tables = [load_lookup_table(look_up_name[0]) for look_up_name in look_up_tables_names]
    process_trips_agglomerate(PATH, table, look_up_tables)

if __name__ == '__main__':
    main()