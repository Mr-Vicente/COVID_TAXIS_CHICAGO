#############################
#   Imports and Contants    #
#############################

# Python modules
import itertools

class Table:
    def __init__(self, header_columns):
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
        if key == -1 or len(self.rows) == 0:
            key = self._next()
            row = f'{key},{str_obj}\n'
            self.rows.append((key, row))
            self.lookup_table[str(key)] = [obj.original_key]
        else:
            print(key)
            print(self.lookup_table[str(key)])
            self.lookup_table[str(key)] = self.lookup_table[str(key)].append(obj.original_key)

