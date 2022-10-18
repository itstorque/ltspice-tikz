from styling import *

class CircuitSchematic:
    
    def __init__(self, symbolstash):
        
        self.elements = set()
        
        self.symbolstash = symbolstash
    
    def add(self, elem):
        
        print(elem)
        
        self.elements.add(elem)

class CircuitElement(CircuitSchematic):
    
    def __init__(self):
        super().__init__()