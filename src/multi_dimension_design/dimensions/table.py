#############################
#   Imports and Contants    #
#############################

# Python modules
import itertools
from src.utils_ import write_dict_2_json_file

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

        if key == -1 or self.lookup_table[str(key)] is None:
            key = self._next()
            row = f'{key},{str_obj}\n'
            self.rows_helper[str_obj] = key
            self.rows.append((key, row))
            self.lookup_table[str(key)] = [obj.original_key]
        else:
            #print(self.lookup_table[str(key)])
            temp = self.lookup_table[str(key)]
            temp.append(obj.original_key)
            self.lookup_table[str(key)] = temp

    def write_lookup_table(self):
        write_dict_2_json_file(self.name, '../lookup_tables')
        print(f'Look up table {self.name} created with success!! :))')

    def write_table(self):
        with open(f'{self.name}.csv', 'w') as f:
            for row in self.rows:
                f.write(row)

    @staticmethod
    def merge_tables(tables):
        old_2_new_key = {}
        new_look_up = {}
        for table in tables:
            print("Table name: ", table.name)
            print("Table rows_helper: ", list(table.rows_helper.items())[:5])
            print("Table lookup: ", list(table.lookup_table.items())[:5])
            rows_helper = table.rows_helper
            for row in rows_helper:
                key = old_2_new_key.get(row, None)
                if not key:
                    key = rows_helper.get(row, None)
                    if not key: continue
                    old_2_new_key[row] = key

                pks = table.lookup_table.get(key, [])
                for pk in pks:
                    keys = new_look_up.get(pk, [])
                    if keys:
                        keys.append(key)
                    else:
                        new_look_up[pk] = [key]
        return new_look_up#,old_2_new_key


