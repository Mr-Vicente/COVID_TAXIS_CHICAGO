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
        key = self._next()
        self.lookup_table[str(key)] = obj.original_key
        row = f'{key},{str(obj)}\n'
        self.rows.append(row)

