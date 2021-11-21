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

    def __str__(self):
        to_string = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        return to_string[self.value]

    def is_weekend(self):
        return self == WEEKDAY.SATURDAY or self == WEEKDAY.SUNDAY

class MONTH(Enum):
    JANUARY = 0
    FEBRUARY = 1
    MARCH = 2
    APRIL = 3
    MAY = 4
    JUNE = 5
    JULY = 6
    AUGUST = 7
    SEPTEMBER = 8
    OCTOBER = 9
    NOVEMBER = 10
    DECEMBER = 11

    def __str__(self):
        to_string = ["january", "february", "march", "april",
                     "may", "june", "july", "august",
                     "september", "october", "november", "december"]
        return to_string[self.value]

class WORLD_STATUS(Enum):
    PRE_COVID = "pre-covid"
    COVID_ERA = "covid"

class FACILITY(Enum):
    HOSPITAL = "hospital"
    CLINIC = "clinic"
    VAX_SITE = "vax_site"
    TEST_SITE = "test_site"
