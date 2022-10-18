import numpy as np
from styling import *

# TODO: add coordinate object...
class Geometry:
    # TODO: implement rotation
    
    def __init__(self, parent=None, linestyle=LineStyle.default, color=Colors.unassigned, geometries=None) -> None:
        
        self.linestyle = linestyle
        self.color = color
        self.line_cap = "square"
        self.thickness = 1
        self.parent = parent
        
        # TODO: not used as of now...
        self.has_children = False 
    
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
    def from_ltspice_gui_command(self, coords, *args, **kwargs):
        # a class method that initializes asy and asc Geometrys
        # TODO: this is not doing anything as of now... Change inehrent resolution here? idk...
        
        for i in range(len(coords)):
            try: 
                coords[i] = np.floor(float(coords[i])/50*100)/100
            except:
                coords[i] = coords[i]
        
        style = coords[-1]
        
    @classmethod
    def add_to_parent_from_ltspice_gui_command(self, parent, coords, *args, **kwargs):
        
        geomtery = self.from_ltspice_gui_command(coords, parent=parent, *args, **kwargs)
        
        if geomtery == None:
            print("Geometry error :(")
            return 
        
        if isinstance(geomtery, Geometry):
            return parent.add( geomtery )
        
        for sub_geometry in geomtery:
            parent.add( sub_geometry )
        
        return True
    
class Line(Geometry):
    
    def __init__(self, point1, point2, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
        self.start = (point1[0], point1[1])
        self.end   = (point2[0], point2[1])
        
    def move_to(self, pos):
        
        self.start = ( self.start[0]+pos[0], self.start[1]+pos[1] )
        self.end   = (   self.end[0]+pos[0],   self.end[1]+pos[1] )
        
    @classmethod
    def from_ltspice_gui_command(self, coords, *args, **kwargs):
        # super().from_ltspice_gui_command(coords)
        
        # linestyle = LineStyle(coords[0]) # TODO: check what NORMAL does in LINE syntax...
        
        coords = [float(i) for i in coords[1:5]]
        
        return Line(coords[0:2], coords[2:4], *args, **kwargs)#, linestyle=linestyle)
        
    def tikz(self) -> str:
        return f"\draw ({self.start[0]},{self.start[1]}) to ({self.end[0]},{self.end[1]});"
    
    def __str__(self):
        return f"LINE ({self.start[0]},{self.start[1]}) to ({self.end[0]},{self.end[1]})"
    
class Arc(Geometry):
    
    def __init__(self, center, size, theta_span, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
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
        
    def move_to(self, pos):
        self.center[0] += pos[0]
        self.center[1] += pos[1]
        
    @classmethod
    def from_ltspice_gui_command(self, coords, *args, **kwargs):
        
        coords = [float(i) for i in coords[1:9]]
        
        pos = np.array(coords[0:2])
                
        size = abs(pos - coords[2:4])/2
        
        center = (pos + coords[2:4])/2
        
        angle = lambda v: np.degrees(np.arctan2(v[1], v[0]))
        
        theta_i = angle(coords[6:8]-center)
        theta_f = angle(coords[4:6]-center)
        
        return Arc(center=center, size=size, theta_span=(theta_i, theta_f), *args, **kwargs)
        
    def tikz(self) -> str:
        return f"\draw ({self.center[0]},{self.center[1]}) [partial ellipse={self.theta_span[0]}:{self.theta_span[1]}:{self.size[0]} and {self.size[1]}];"
        
class Circle(Arc):
    
    def __init__(self, center, size, *args, **kwargs):
        super().__init__(center, size, theta_span=(0, 360), *args, **kwargs)
        
    @classmethod
    def from_ltspice_gui_command(self, coords, *args, **kwargs):
        # SPICE COMMAND EXAMPLE FOR current source
        # at loc 1248, 16 rotated 90deg: 
        # SYMBOL current 1248 16 R90
        
        coords = [float(i) for i in coords[1:5]]

        pos = np.array(coords[0:2])
        size = abs(pos - coords[2:4])/2
        
        pos += size
        
        return Circle(center=pos, size=size, *args, **kwargs)
        
    def tikz(self) -> str:
        return f"\draw ({self.center[0]},{self.center[1]}) ellipse ({self.size[0]} and {self.size[1]});"

class Rectangle(Line):
    # A rectangle is defined by 2 corners, given a Line, it can only correspond to one line...
    pass
    
        
class Symbol(Geometry):
    
    def __init__(self, parent, *args, **kwargs) -> None:
        super().__init__(parent=parent, *args, **kwargs)
        
        if "geometries" in kwargs:
            self.geometries = kwargs["geometries"]
            
            for geom in self.geometries:
                geom.move_to(self.pos)
                
        else:
            self.geometries = set()
        
        self.has_children = True
        
    @classmethod
    def from_ltspice_gui_command(self, cmd, parent, *args, **kwargs):
        
        self.parent = parent
        
        # TODO: set parent of sub-lines to component...
        
        component_name = cmd[0]
        coords = [float(i) for i in cmd[1:3]]
        rotation = cmd[3]
        
        self.pos = coords
        self.rotation = rotation # TODO: implement rotating a symbol
        
        symbol = parent.symbolstash.get_symbol(component_name)
        
        if symbol:
            
            # This is being sent in with Symbol!
            kwargs["geometries"] = symbol.geometries
            
            return Symbol(parent=parent, *args, **kwargs)
        
    def draw(self):
        
        return '\n'.join([ geom.draw() for geom in self.geometries ])
    
class Wire(Line):
    
    @classmethod
    def from_ltspice_gui_command(self, coords, *args, **kwargs):
        return super().from_ltspice_gui_command( [0] + coords, *args, **kwargs )

class Text(Geometry):
    pass

class Flag(Text):
    pass