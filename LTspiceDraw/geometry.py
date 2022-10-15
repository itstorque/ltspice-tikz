import numpy as np
from matplotlib.lines import lineStyles
from styling import *

class Geometry:
    
    def __init__(self, linestyle=LineStyle.solid, color=Colors.black) -> None:
        
        self.linestyle = linestyle
        self.color = color
    
    def set_style(self, style):
        if style in LineStyle:
            self.linestyle = style
        else:
            self.linestyle = LineStyle(style)
    
    def styling(self) -> None:
        return self.linestyle
    
    def color(self) -> None:
        return self.color
    
    def tikz(self) -> str:
        return ""
    
    @classmethod
    def from_coords(self, coords):
        # a class method that initializes asy and asc Geometrys
        
        coords = [np.floor(float(c)/50*100)/100 for c in coords]
        
        self.set_style(coords[-1])
    
class Line(Geometry):
    
    def __init__(self, point1, point2, linestyle=LineStyle.solid, color=Colors.black) -> None:
        super().__init__(linestyle, color)
        
        self.start = point1
        self.end   = point2
    
class Arc(Geometry):
    
    def __init__(self, center, size, theta_span, linestyle=LineStyle.solid, color=Colors.black) -> None:
        super().__init__(linestyle, color)
        
        try:
            self.theta_span = (theta_span[0], theta_span[1])
        except:
            self.theta_span = (0, theta_span)
        
        try:
            self.size = (size[0], size[1])
        except:
            self.size = (size, size)
            
        self.center = center
        self.size = size
        
    def tikz(self) -> str:
        return f"\draw ({self.center[0]},{self.center[1]}) [partial ellipse={self.theta_span[0]}:{self.theta_span[1]}:{self.size[0]} and {self.size[1]}];"
        
class Circle(Arc):
    
    def __init__(self, center, size, linestyle=LineStyle.solid, color=Colors.black) -> None:
        super().__init__(center, size, theta_span=(0, 360), linestyle=linestyle, color=color)
        
    @classmethod
    def from_coords(self, coords):
        
        super().from_coords(coords)

        pos = np.array(coords[0:2])
        size = abs(pos - coords[2:4])/2
        
        pos += size
        
    def tikz(self) -> str:
        return f"\draw ({self.center[0]},{self.center[1]}) ellipse ({self.size[0]} and {self.size[1]});"
        
        