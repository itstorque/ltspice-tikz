# TODO: add coordinate object...
class Geometry:
    
    def __init__(self, linestyle=LineStyle.solid, color=Colors.unassigned) -> None:
        
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
    def from_ltspice_gui_command(self, coords):
        # a class method that initializes asy and asc Geometrys
        
        coords = [math.floor(float(c)/50*100)/100 for c in coords]
        
        style = coords[-1]
    
class Line(Geometry):
    
    def __init__(self, point1, point2, linestyle=LineStyle.solid, color=Colors.unassigned) -> None:
        super().__init__(linestyle, color)
        
        self.start = point1
        self.end   = point2
        
    @classmethod
    def from_ltspice_gui_command(self, coords):
        super().from_ltspice_gui_command(coords)
        
        return Line(coords[2:4], coords[4:6])
        
    def tikz(self) -> str:
        return f"\draw ({self.start[0]},{self.start[1]}) to ({self.end[0]},{self.end[1]});"
    
class Arc(Geometry):
    
    def __init__(self, center, size, theta_span, linestyle=LineStyle.solid, color=Colors.unassigned) -> None:
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
        
    @classmethod
    def from_ltspice_gui_command(self, coords):
        super().from_ltspice_gui_command(coords)
        
        pos = coords[0:2]
                
        size = abs(pos - coords[2:4])/2
        
        center = (pos + coords[2:4])/2
        
        theta_i = angle(coords[6:8]-center)
        theta_f = angle(coords[4:6]-center)
        
        return Arc(center=center, size=size, theta_span=(theta_i, theta_f))
        
    def tikz(self) -> str:
        return f"\draw ({self.center[0]},{self.center[1]}) [partial ellipse={self.theta_span[0]}:{self.theta_span[1]}:{self.size[0]} and {self.size[1]}];"
        
class Circle(Arc):
    
    def __init__(self, center, size, linestyle=LineStyle.solid, color=Colors.unassigned) -> None:
        super().__init__(center, size, theta_span=(0, 360), linestyle=linestyle, color=color)
        
    @classmethod
    def from_ltspice_gui_command(self, coords):
        
        super().from_ltspice_gui_command(coords)

        pos = coords[0:2]
        size = [abs(i - j)/2 for i, j in zip(pos, coords[2:4])]
        
        pos += size
        
        return Circle(center=pos, size=size)
        
    def tikz(self) -> str:
        return f"\draw ({self.center[0]},{self.center[1]}) ellipse ({self.size[0]} and {self.size[1]});"
        
class Symbol(Geometry):
    
    def __init__(self, linestyle=LineStyle.solid, color=Colors.black) -> None:
        super().__init__(linestyle, color)
        
        self.geometries = set()
        
    def add(self, geom):
        self.geometries.add(geom)
        
    def draw(self):
        
        return '\n'.join([ geom.draw() for geom in self.geometries ])