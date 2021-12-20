
from src.utils_ import timing_decorator, read_json_file_2_dict
def load_lookup_table(look_up_table_path:str):
    return read_json_file_2_dict(look_up_table_path, store_dir='./lookup_tables')

def blocks(files, size=65536):
    while True:
        b = files.read(size)
        if not b: break
        yield b

def get_number_of_lines(filename):
    with open(filename, "r",encoding="utf-8",errors='ignore') as f:
        return sum(bl.count("\n") for bl in blocks(f)) - 1