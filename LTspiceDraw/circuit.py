from styling import *

class CircuitSchematic:
    
    def __init__(self, symbolstash):
        
        self.geometries = set()
        
        self.symbolstash = symbolstash
    
    def add(self, elem):
        
        self.geometries.add(elem)

class CircuitElement(CircuitSchematic):
    
    def __init__(self):
        super().__init__()