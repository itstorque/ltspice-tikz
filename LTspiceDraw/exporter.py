from geometry import *

class Exporter:
    def __init__(self):
        pass    
    
    def draw_line(self, line):
        pass
    
    def draw_arc(self, arc):
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
                
class HTML_Canvas_Exporter(Exporter):
    def __init__(self, ctx):
        self.ctx = ctx
    
    def draw_line(self, line):
        
        print(line)
        
        self.ctx.beginPath()
        self.ctx.lineWidth = line.thickness
        self.ctx.lineCap = line.line_cap
        self.ctx.moveTo(*line.start)
        self.ctx.lineTo(*line.end)
        self.ctx.stroke()
    
class tikz_Exporter(Exporter):
    pass