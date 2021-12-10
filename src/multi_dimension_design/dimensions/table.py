#############################
#   Imports and Contants    #
#############################

# Python modules
import itertools
from src.utils import write_dict_2_json_file

class Table:
    def __init__(self, header_columns, name):
        self.name = name
        self.succ = itertools.count()
        self.header_columns = header_columns
        self.rows = []
        self.lookup_table = {}

    def _next(self):
        return next(self.succ)

    def insert(self, obj):
        str_obj = str(obj)
        key = -1
        for row in self.rows:
            if str_obj in row[-1]:
                key = row[0]
                break

        if key == -1 or self.lookup_table[str(key)] is None:
            key = self._next()
            row = f'{key},{str_obj}\n'
            self.rows.append((key, row))
            self.lookup_table[str(key)] = [obj.original_key]
        else:
            print(self.lookup_table[str(key)])
            temp = self.lookup_table[str(key)]
            temp.append(obj.original_key)
            self.lookup_table[str(key)] = temp

    def write_lookup_table(self):
        write_dict_2_json_file(self.name, '../lookup_tables')
        print(f'Look up table {self.name} created with success!! :))')

