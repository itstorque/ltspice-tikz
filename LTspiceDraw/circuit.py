from geometry import *
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
        
        self.backgroundColor = Colors.unassigned
        
        self.commentColor = Colors.unassigned
        self.commandColor = Colors.unassigned
        
    def textColor(self, type):
        if type == TextNetlist.Command:
            return self.commandColor
        elif type == TextNetlist.Comment:
            return self.commentColor
        
    def set_color(self, color):
        # TODO: add check to see if color is instance of Color or Colors...
        self.color = Color(color)
    
    def add(self, elem):
        
        self.geometries.add(elem)

class OrderedCircuitSchematic(CircuitSchematic):
    
    def __init__(self, symbolstash):
        super().__init__(symbolstash)
        
        # dict that stores node loc -> geometries at that loc
        self.node_elements = {} 
        
    def add(self, elem):
        super().add(elem)
        
        for port in elem.ports:
            
            if port.loc in self.node_elements:
                self.node_elements[port.loc].add(port)
            else:
                self.node_elements[port.loc] = port

class CircuitElement(CircuitSchematic):
    
    def __init__(self):
        super().__init__()