
#############################
#   Imports and Contants    #
#############################

# Python modules
import time
import os
import json

#############################
#   Files Managment         #
#############################

def create_directory(output_dir):
    # Create output directory if needed
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


def write_dict_2_json_file(json_object, filename, store_dir='.'):
    create_directory(store_dir)
    with open(f'{store_dir}/{filename}.json', 'w', encoding='utf-8') as file:
        json.dump(json_object, file, ensure_ascii=False, indent=4)


def read_json_file_2_dict(filename, store_dir='.'):
    create_directory(store_dir)
    with open(f'{store_dir}/{filename}.json', 'r', encoding='utf-8') as file:
        return json.load(file)


#############################
#         Timing
#############################

def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        original_return_val = func(*args, **kwargs)
        end = time.time()
        print("time elapsed in ", func.__name__, ": ", end - start, sep='')
        return original_return_val

    return wrapper