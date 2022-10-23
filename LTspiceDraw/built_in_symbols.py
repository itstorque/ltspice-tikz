from enum import Enum

class SYMBOLS(Enum):

    GND = """LINE Normal 0 0 0 4 2
    LINE Normal -12 4 12 4 2
    LINE Normal -12 4 0 16 2
    LINE Normal 0 16 12 4 2"""

    NODE = """LINE Normal -4 4 4 4 2
    LINE Normal -4 4 -4 -4 2
    LINE Normal 4 4 4 -4 2
    LINE Normal -4 -4 4 -4 2"""
    
    def __call__(self):
        return self.value