#############################
#   Imports and Contants    #
#############################

# Python modules
import itertools
from src.utils_ import write_dict_2_json_file,create_directory
from collections import Counter
class Table:
    def __init__(self, header_columns, name, offset):
        self.name = name
        self.succ = itertools.count(offset)
        self.header_columns = header_columns
        self.rows = []
        self.rows_helper = {}
        self.lookup_table = {}

    def _next(self):
        return next(self.succ)

    def insert_2(self, obj):
        str_obj = str(obj)
        key = self.rows_helper.get(str_obj, -1)
        if key == -1:
            key = self._next()
            row = f'{key},{str_obj}\n'
            self.rows_helper[str_obj] = key
            self.rows.append(row)
            self.lookup_table[obj.original_key] = [str(key)]
        else:
            if not self.lookup_table.get(obj.original_key, []):
                self.lookup_table[obj.original_key] = [str(key)]
            else:
                self.lookup_table[obj.original_key].append(str(key))


    def insert(self, obj):
        str_obj = str(obj)
        key = self.rows_helper.get(str_obj, -1)

        if key == -1:
            key = self._next()
            self.rows_helper[str_obj] = key
            self.lookup_table[str(key)] = obj.original_key

    def write_own_lookup_table(self):
        Table.write_lookup_table(self.lookup_table, self.name)

    def write_own_table(self):
        Table.write_table(self.rows_helper, self.name)

    @staticmethod
    def write_lookup_table(look_up, name):
        write_dict_2_json_file(look_up, name, '../../../lookup_tables')
        print(f'Look up table {name} created with success!! :))')

    @staticmethod
    def write_table(rows_helper, name, store_dir='../../../dimensions'):
        create_directory(store_dir)
        with open(f'{store_dir}/{name}.csv', 'w') as f:
            for str_obj, key in rows_helper.items():
                f.write(f'{key},{str_obj}\n')

    @staticmethod
    def merge_tables(tables, dimension_name):
        new_rows_helper = {}
        new_look_up = {}
        for table in tables:
            #print(table.lookup_table)
            for row, stored_key in table.rows_helper.items():
                key = new_rows_helper.get(row, None)
                if key is None:
                    key = stored_key
                    new_rows_helper[row] = key

                pk = table.lookup_table.get(str(stored_key), -1)
                key_ = new_look_up.get(str(pk), -1)
                if key_ == -1:
                    new_look_up[str(pk)] = [str(key)]
        Table.write_table(new_rows_helper, dimension_name)
        Table.write_lookup_table(new_look_up, dimension_name)


