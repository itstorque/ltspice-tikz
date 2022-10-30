# NOTE: when you edit a symbol in here, it won't
# take effect until you reload symbols. Eventually
# add a method to update this user side...

from enum import Enum

class SYMBOLS(Enum):

    GND = """
    LINE Normal -12 0 12 0 2
    LINE Normal -12 0 0 12 2
    LINE Normal 0 12 12 0 2
    """

    NODE = """
    LINE Normal -4 4 4 4 2
    LINE Normal -4 4 -4 -4 2
    LINE Normal 4 4 4 -4 2
    LINE Normal -4 -4 4 -4 2
    """
    
    def __call__(self):
        return self.value