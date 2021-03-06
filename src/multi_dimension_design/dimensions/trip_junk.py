#############################
#   Imports and Contants    #
#############################

# Python modules
from dataclasses import dataclass

# Local module

@dataclass
class Trip_Junk:
    """Representing the junk dimension in multimodal design"""
    original_key: int
    payment_type: str
    company: str

    def __str__(self):
        return f'{self.payment_type},' \
               f'{self.company}'


