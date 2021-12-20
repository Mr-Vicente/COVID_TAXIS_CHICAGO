#############################
#   Imports and Contants    #
#############################

# Python modules
import datetime
import holidays

# Local module
from src.multi_dimension_design.dimensions.utils_ import WEEKDAY, MONTH
from src.utils_ import read_json_file_2_dict, chunks

phases = read_json_file_2_dict('covid_phases', '../data')

class Date:
    """Representing the date dimension in multimodal design"""
    original_key: str
    year: int
    day_of_the_month: int
    day_of_the_week: WEEKDAY
    is_weekend: bool
    is_holiday: bool
    pandemic_phase: str

    def __init__(self, original_key, date):
        self.original_key = original_key
        self.covid_phases = phases
        self._parse_date(date)

    def _parse_date(self, date):
        parsed_date = datetime.datetime.strptime(date, "%m/%d/%Y %I:%M:%S %p")
        self.year = parsed_date.year
        self.month = MONTH(parsed_date.month-1)
        self.day_of_the_month = parsed_date.day
        self.day_of_the_week = WEEKDAY(parsed_date.weekday())
        self.is_weekend = self.day_of_the_week.is_weekend()

        # Select country
        us_holidays = holidays.US()
        self.is_holiday = f'{parsed_date.day}-{parsed_date.month}-{parsed_date.year}' in us_holidays

        #covid phase
        phase = self.parse_covid_phases(parsed_date, self.covid_phases)
        self.pandemic_phase = self.parse_covid_phase(phase)

    def parse_covid_phase(self, phase):
        if isinstance(phase, list):
            phase = phase[0]
        return phase.get('class', '')


    def parse_covid_phases(self, curr_date, covid_phases):
        assert isinstance(covid_phases, dict)
        dates = []
        for ((date_f, phase_f),(date_e, phase_e)) in chunks(list(covid_phases.items()),2):
            parsed_date_f = datetime.datetime.strptime(date_f, "%d-%m-%Y")
            parsed_date_e = datetime.datetime.strptime(date_e, "%d-%m-%Y")
            dates.append(parsed_date_f)
            if parsed_date_f <= curr_date < parsed_date_e:
                return phase_f
        if curr_date < dates[0]:
            return {'class': 'Pre-covid', 'description': 'Pandemic free'}
        else:
            return phase_e


    def __str__(self):
        return f'{self.year},' \
               f'{self.month},' \
               f'{self.day_of_the_month},' \
               f'{self.day_of_the_week},' \
               f'{self.is_weekend},' \
               f'{self.is_holiday},' \
               f'{self.pandemic_phase}'


