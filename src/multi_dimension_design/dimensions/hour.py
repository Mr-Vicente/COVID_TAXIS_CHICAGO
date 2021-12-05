#############################
#   Imports and Contants    #
#############################

# Python modules
import datetime

class Hour:
    original_key: str
    hour: int
    minute: int
    is_rush_hour: bool

    def __init__(self, original_key, date):
        self.original_key = original_key
        self._parse_date(date)

    def _parse_date(self, date):
        parsed_date = datetime.datetime.strptime(date, "%m/%d/%Y %I:%M:%S %p")
        self.hour = parsed_date.hour
        self.minute = parsed_date.minute
        self.is_rush_hour = self.rush_hour(self.hour)

    def rush_hour(self, hour):
        return (7 <= hour <= 10) or (17 <= hour <= 19)

    def __str__(self):
        return f'{self.hour},' \
               f'{self.minute},' \
               f'{self.is_rush_hour},'