#############################
#   Imports and Contants    #
#############################

# Python modules
from enum import Enum

class WEEKDAY(Enum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6

    def __init__(self):
        self.to_string = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

    def __str__(self):
        return self.to_string[self.value]

    def is_weekend(self):
        return self == WEEKDAY.SATURDAY or self == WEEKDAY.SUNDAY

class WORLD_STATUS(Enum):
    PRE_COVID = "pre-covid"
    COVID_ERA = "covid"

class FACILITY(Enum):
    HOSPITAL = "hospital"
    CLINIC = "clinic"
    VAX_SITE = "vax_site"
    TEST_SITE = "test_site"
