from geometry import *

class Exporter:
    def __init__(self):
        pass    
    
    def draw_line(self, line):
        pass
    
    def draw_arc(self, arc):
        pass
    
    def draw_rectangle(self, rectangle):
        pass
    
    def draw_circle(self, circle):
        pass
    
    def add_text(self, text_object):
        pass
    
    def draw(self, schematic):
        
        print("EXPORTER.DRAW")
        
        for elem in schematic.elements:
            
            print(type(elem))
            
            if type(elem) == Line:
                self.draw_line(elem)
                
            elif type(elem) == Circle:
                self.draw_circle(elem)
                
class HTML_Canvas_Exporter(Exporter):
    def __init__(self, ctx):
        self.ctx = ctx
    
    def draw_line(self, line):
        
        self.ctx.beginPath()
        self.ctx.lineWidth = line.thickness
        self.ctx.lineCap = line.line_cap
        self.ctx.moveTo(*line.start)
        self.ctx.lineTo(*line.end)
        self.ctx.stroke()
    
    def draw_rectangle(self, rectangle):
        
        self.ctx.beginPath()
        self.ctx.rect(*rectangle.start, *rectangle.end)
        self.ctx.stroke()
    
    def draw_circle(self, circle):
        
        self.ctx.beginPath()
        self.ctx.arc(*circle.center, circle.size[0], 0, 2 * np.pi)
        self.ctx.stroke()
        
        # self.draw_arc(circle)
        
    def draw_arc(self, arc):
        
        rotation = 0 # TODO: add rotation...
        
        self.ctx.beginPath()
        self.ctx.ellipse(*arc.center, *arc.size, rotation, 0, 2 * np.pi)
        self.ctx.stroke()
    
class tikz_Exporter(Exporter):
    pass