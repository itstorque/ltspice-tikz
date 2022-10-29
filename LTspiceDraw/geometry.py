import numpy as np
from styling import *
    
class TextNetlist(Enum):
    Unknown    = -1
    Comment    = 0
    Command    = 1
    SymbolText = 2
    Flag       = 3

# TODO: add coordinate object...
# TODO: probably remove all *args...
# TODO: port all tikz calls to a new TikzExporter
class Geometry:
    # TODO: implement rotation
    
    def __init__(self, parent=None, linestyle=LineStyle.default, color=Colors.unassigned, geometries=None, *args, **kwargs) -> None:
        
        self.linestyle = linestyle
        self.color = color
        self.line_cap = "square"
        self.thickness = 1
        self.parent = parent
        
        self.rotation = 0
        self.reflected = False
        
        self.default_sensitivity = 5
        
        self.name = kwargs["name"] if "name" in kwargs else "Geometry"
        
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
    
    def set_color(self, color):
        self.color = color
        
    def is_inside(self, x, y, sensitivity = 5):
        return False
    
    def in_bounding_box(self, pt1, pt2, test_pt, sensitivity=None):
        
        if sensitivity == None: sensitivity = self.default_sensitivity
        
        self.pt1 = pt1 - sensitivity
        self.pt2 = pt2 + sensitivity
        
        return (test_pt[0] > pt1[0] - sensitivity and test_pt[0] < pt2[0] + sensitivity and test_pt[1] > pt1[1] - sensitivity and test_pt[1] < pt2[1] + sensitivity)
    
    @classmethod
    def from_ltspice_gui_command(self, coords, *args, **kwargs):
        # a class method that initializes asy and asc Geometrys
        pass
        
        # transformation = coords[-1]
        
        # # print(coords)
        # # print(">>>", transformation, transformation[0])
        
        # if transformation[0] == "R":
        #     # rotated
        #     self.rotation = float(transformation[1:])
        #     self.reflected = True
        # elif transformation[0] == "M":
        #     # reflected and rotated
        #     self.rotation = float(transformation[1:])
        #     self.reflected = False
        
        # TODO: migrate to better code snapping in here instead of in children...
        # for i in range(len(coords)):
        #     try: 
        #         coords[i] = np.floor(float(coords[i])/50*100)/100
        #     except:
        #         coords[i] = coords[i]
        
        # style = coords[-1]
        
    @classmethod
    def add_to_parent_from_ltspice_gui_command(self, parent, coords, *args, **kwargs):
        
        geometry = self.from_ltspice_gui_command(coords, parent=parent, *args, **kwargs)
        
        geometry.set_color(parent.color)
        
        if geometry == None:
            print("Geometry error :(")
            return
        
        if isinstance(geometry, Geometry):
            return parent.add( geometry )
        
        for sub_geometry in geometry:
            parent.add( sub_geometry )
        
        return True
    
class Line(Geometry):
    
    def __init__(self, point1, point2, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
        self.start = Coord(point1[0], point1[1])
        self.end   = Coord(point2[0], point2[1])
        
    # def move_to(self, pos):
        
    #     self.start = ( self.start[0]+pos[0], self.start[1]+pos[1] )
    #     self.end   = (   self.end[0]+pos[0],   self.end[1]+pos[1] )
        
    @classmethod
    def from_ltspice_gui_command(self, coords, *args, **kwargs):
        # super().from_ltspice_gui_command(coords, *args, **kwargs)
        
        # linestyle = LineStyle(coords[0]) # TODO: check what NORMAL does in LINE syntax...
        
        coords = Coord(coords[1:5])
        
        return Line(coords[0:2], coords[2:4], *args, **kwargs)#, linestyle=linestyle)
        
    def is_inside(self, x, y, sensitivity = None):
        return self.in_bounding_box(self.start.as_array(), self.end.as_array(), (x, y), sensitivity=sensitivity)
        
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
            
        self.center = Coord(center)
        self.size = Coord(size)
        
    def is_inside(self, x, y, sensitivity = None):
        return self.in_bounding_box(self.center.as_array() - self.size.as_array(), self.center.as_array() + self.size.as_array(), (x, y), sensitivity=sensitivity)
        
    # def move_to(self, pos):
    #     self.center[0] += pos[0]
    #     self.center[1] += pos[1]
        
    @classmethod
    def from_ltspice_gui_command(self, coords, *args, **kwargs):
        # super().from_ltspice_gui_command(coords, *args, **kwargs)
        
        coords = Coord(coords[1:9])
        
        pos = coords[0:2].as_array()
                
        size = abs(pos - coords[2:4])/2
        
        center = (pos + coords[2:4])/2
        
        angle = lambda v: np.arctan2(v[1], v[0])
        
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
        # Geometry.from_ltspice_gui_command(coords, *args, **kwargs)
        # SPICE COMMAND EXAMPLE FOR current source
        # at loc 1248, 16 rotated 90deg: 
        # SYMBOL current 1248 16 R90
        
        coords = Coord(coords[1:5])

        pos = coords[0:2].as_array()
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
        # TODO: inherit SChematic???
        
        self.backgroundColor = None
        
        if "geometries" in kwargs:
            self.geometries = kwargs["geometries"]
            
            # for geom in self.geometries:
            #     geom.move_to(self.pos)
                
        else:
            self.geometries = set()
        
        self.has_children = True
        
        if "pos" in kwargs: 
            self.pos = Coord(kwargs["pos"])
        else: 
            self.pos = Coord(0, 0)
        
        if "rotation" in kwargs: 
            self.rotation = kwargs["rotation"]
        else: 
            self.rotation = 0
        
        if "reflected" in kwargs: 
            self.reflected = kwargs["reflected"]
        else: 
            self.reflected = False
        
    def is_inside(self, x, y, sensitivity = None):
        
        x, y = x - self.pos[0], y - self.pos[1]
        
        if self.reflected: 
            x, y = -x, y
            
        if self.rotation:
            r = -np.deg2rad(self.rotation)
            R = np.array([[np.cos(r), -np.sin(r)],
                          [np.sin(r),  np.cos(r)]])
            x, y = R @ np.array([x, y])
        
        # print(x, y)
        
        pt_x_storage = set()
        pt_y_storage = set()
        ans = False
        
        for geom in self.geometries:
            
            ans = ans or geom.is_inside(x, y, sensitivity=sensitivity)
            
            pt_x_storage.add(geom.pt1[0])
            pt_x_storage.add(geom.pt2[0])
            
            pt_y_storage.add(geom.pt1[1])
            pt_y_storage.add(geom.pt2[1])
            
        self.pt1 = (min(pt_x_storage), min(pt_y_storage))# + self.pos.as_array()
        self.pt2 = (max(pt_x_storage), max(pt_y_storage))# + self.pos.as_array()
        
        if self.rotation:
            r = np.deg2rad(self.rotation)
            R = np.array([[np.cos(r), -np.sin(r)],
                          [np.sin(r),  np.cos(r)]])
            
            self.pt1 = R @ self.pt1
            self.pt2 = R @ self.pt2
        
        if self.reflected:
            self.pt1 = [-self.pt1[0], self.pt1[1]]
            self.pt2 = [-self.pt2[0], self.pt2[1]]
            
        self.pt1 = self.pos.as_array()+self.pt1
        self.pt2 = self.pos.as_array()+self.pt2
            
            
        return ans # self.in_bounding_box(self.pt1, self.pt2, (x, y), sensitivity=sensitivity)
        
    @classmethod
    def from_ltspice_gui_command(self, cmd, parent, *args, **kwargs):
        # super().from_ltspice_gui_command(cmd, *args, **kwargs)
        
        component_name = cmd[0]
        coords = Coord(cmd[1:3])
        transformation = cmd[-1]
        
        kwargs["name"] = component_name
        
        if transformation[0] == "R":
            # rotated
            kwargs["rotation"] = float(transformation[1:])
            kwargs["reflected"] = False
        elif transformation[0] == "M":
            # reflected and rotated
            kwargs["rotation"] = float(transformation[1:])
            kwargs["reflected"] = True
        
        self.parent = parent
        
        # TODO: set parent of sub-lines to component...
        
        kwargs["pos"] = coords
        
        symbol = parent.symbolstash.get_symbol(component_name)
        
        if symbol:
            
            # This is being sent in with Symbol!
            kwargs["geometries"] = symbol.geometries
            
            return Symbol(parent=parent, *args, **kwargs)
    
    def set_color(self, color):
        self.color = color
        for geom in self.geometries:
            geom.color = color
        
    def draw(self):
        
        return '\n'.join([ geom.draw() for geom in self.geometries ])
    
class Wire(Line):
    
    def __init__(self, point1, point2, *args, **kwargs) -> None:
        super().__init__(point1, point2, *args, **kwargs)
        
        self.ports = { # wire has two ports, a symmetric input and output port
            Port(self, Coord(point1), "0"),
            Port(self, Coord(point2), "1")
        }
    
    @classmethod
    def from_ltspice_gui_command(self, coords, *args, **kwargs):
        return super().from_ltspice_gui_command( [0] + coords, *args, **kwargs )

class Text(Geometry):
    
    def __init__(self, anchor, text, text_align="left", font_size=20, color=Colors.unassigned, type=TextNetlist.Unknown, **kwargs) -> None:
        super().__init__(**kwargs)
        
        self.pos  = anchor
        self.text = text
        
        self.font_size = font_size
        self.text_align = text_align
        
        self.color = color
        
        self.type = type
        
    def get_pos(self, loc):
        
        match loc:
            case "top left": 
                return self.pos
            case "left":
                return Coord(self.pos[0], self.pos[1] + self.font_size/2)
    
    @classmethod
    def from_ltspice_gui_command(self, cmd, *args, **kwargs):
        # TEXT 152 552 Left 2 !comment with spaces in it
        
        font_size = [0.625, 1, 1.5, 2, 2.5, 3.5, 5, 7][int(cmd[3])] * 12
        
        text = ' '.join(cmd[4:])
        
        if text[0] == ";": 
            type = TextNetlist.Comment
            text = text[1:]
        elif text[0] == "!": 
            type = TextNetlist.Command
            text = text[1:]
        
        return Text(Coord(cmd[0], cmd[1]), text, text_align=cmd[2].lower(), font_size=font_size, type=type)

class Flag(Text, Symbol):
    
    def __init__(self, parent, pos, name, color=Colors.unassigned, **kwargs):
        
        super().__init__(parent=parent, anchor=pos, text=name, text_align="left", font_size=20, color=Colors.unassigned, type=TextNetlist.Flag, **kwargs)
        
        self.parent = parent
        
        self.is_ground = False
        
        self.geometries = parent.symbolstash.get_symbol("NODE").geometries
    
    @classmethod
    def from_ltspice_gui_command(self, cmd, parent, *args, **kwargs):
        
        name = ' '.join(cmd[2:])
        
        if name == "0":
            return Ground(parent, Coord(cmd[0:2]))
        
        return Flag(parent, Coord(cmd[0:2]), name)

class Ground(Flag):
    
    def __init__(self, parent, pos, color=Colors.unassigned, **kwargs):
        
        super().__init__(parent, pos, "GND", color, **kwargs)
    
        self.geometries = parent.symbolstash.get_symbol("GND").geometries

class Port(Flag):
    
    def __init__(self, parent, pos, name):
        
        self.parent = parent
        self.pos = pos
        self.name = name
        
class Coord(tuple):
    
    def __new__(self, *args):
        if (isinstance(args[0], Coord      ) or \
            isinstance(args[0], np.ndarray ) or \
            isinstance(args[0], list       ) or \
            isinstance(args[0], tuple      ) ) and len(args)==1:
            # return tuple.__new__(Coord, args[0])
            args = args[0]
        
        return tuple.__new__(Coord, (float(i) for i in args))
    
    def as_array(self):
        return np.array(self)
    
    def __getitem__(self, *args):
        
        if not isinstance(args[0], slice):
            return super().__getitem__(*args)
        
        return Coord(*super().__getitem__(*args))