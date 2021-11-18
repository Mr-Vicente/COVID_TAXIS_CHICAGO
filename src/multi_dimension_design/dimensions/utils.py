#############################
#   Imports and Contants    #
#############################

# Python modules
from enum import Enum

class WEEKDAY(Enum):
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"

    def is_weekend(self):
        return self == WEEKDAY.SATURDAY or self == WEEKDAY.SUNDAY

class WORLD_STATUS(Enum):
    PRE_COVID = "pre-covid"
    COVID_ERA = "covid"