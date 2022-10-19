from styling import *

class CircuitSchematic:
    
    def __init__(self, symbolstash):
        
        self.geometries = set()
        
        self.symbolstash = symbolstash
        
        self.pos = (0, 0)
        
        self.rotation = 0
        self.reflected = False
        
        self.name = "CircuitSchematic"
        
        self.color = Colors.unassigned
        
    def set_color(self, color):
        # TODO: add check to see if color is instance of Color or Colors...
        self.color = Color(color)
    
    def add(self, elem):
        
        self.geometries.add(elem)

class CircuitElement(CircuitSchematic):
    
    def __init__(self):
        super().__init__()