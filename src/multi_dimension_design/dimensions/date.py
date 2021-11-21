#############################
#   Imports and Contants    #
#############################

# Python modules
import datetime
import holidays

# Local module
from src.multi_dimension_design.dimensions.utils import WEEKDAY

class Date:
    """Representing the date dimension in multimodal design"""
    original_key: str
    year: int
    day_of_the_month: int
    day_of_the_week: WEEKDAY
    is_weekend: bool
    is_holiday: bool
    def __init__(self, original_key, date):
        self._parse_date(date)
    def _parse_date(self, date):
        parsed_date = datetime.datetime.strptime(date, "%d/%m/%Y %I:%M:%S %p")
        self.year = parsed_date.year
        self.day_of_the_month = parsed_date.day
        self.day_of_the_week = WEEKDAY[parsed_date.weekday()]
        self.is_weekend = self.day_of_the_week.is_weekend()

        # Select country
        us_holidays = holidays.US()
        self.is_holiday = f'{parsed_date.day}-{parsed_date.month}-{parsed_date.year}' in us_holidays

    def __str__(self):
        return f'{self.year},' \
               f'{self.day_of_the_month},' \
               f'{self.day_of_the_week},' \
               f'{self.is_weekend},' \
               f'{self.is_holiday}'

