#############################
#   Imports and Contants    #
#############################

# Python modules
from dataclasses import dataclass

# Local module
from src.multi_dimension_design.dimensions.utils import WEEKDAY

@dataclass
class Date:
    """Representing the date dimension in multimodal design"""
    key: int
    day_of_the_month: int
    day_of_the_week: WEEKDAY
    is_weekend: bool
    is_holiday: bool

