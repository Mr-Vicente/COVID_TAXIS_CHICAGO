#############################
#   Imports and Contants    #
#############################

# Python modules
from dataclasses import dataclass

# Local module

@dataclass
class Trip_Junk:
    """Representing the junk dimension in multimodal design"""
    key: int
    payment_type: str
    company: str

