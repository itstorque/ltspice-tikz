from styling import *

class CircuitSchematic:
    
    def __init__(self):
        
        self.elements = set()
    
    def add(self, elem):
        
        print(elem)
        
        self.elements.add(elem)

class CircuitElement(CircuitSchematic):
    
    def __init__(self):
        super().__init__()