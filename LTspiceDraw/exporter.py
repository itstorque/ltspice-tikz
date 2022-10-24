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
        
        if schematic.backgroundColor:
            # self.ctx.fillStyle = schematic.backgroundColor;
            # self.ctx.fillRect(0, 0, self.canvas.width, self.canvas.height);
            self.canvas.style.backgroundColor = schematic.backgroundColor().hex()
        
        # TODO: move these to only be in the HTML_canvas_exporter class
        
        # apply transformation into the frame of reference of the component
        self.ctx.translate(*schematic.pos)
        self.ctx.scale(-1 if schematic.reflected else 1, 1)
        self.ctx.rotate(np.deg2rad(schematic.rotation))
        
        for elem in schematic.geometries:
            
            elem.color().fallback(schematic.color())
            
            self.ctx.strokeStyle = elem.color().hex()
            
            if type(elem) == Line:
                self.draw_line(elem)
                
            elif type(elem) == Circle:
                self.draw_circle(elem)
                
            elif type(elem) == Arc:
                self.draw_arc(elem)
                
            elif type(elem) == Rectangle:
                self.draw_rectangle(elem)
                
            elif type(elem) == Text:
                elem.color().fallback(schematic.textColor(elem.type))
                self.add_text(elem)
                
            elif type(elem) == Ground:
                self.draw(elem)
                
            elif type(elem) == Flag:
                self.draw(elem)
                
            elif type(elem) == Symbol:
                self.draw(elem)
               
        # apply inverse of transformation done before drawing 
        # Order matters... Since we applied translation(x,y), reflect(T), rotate(θ)
        # we need to apply (translation(x,y), reflect(T), rotate(θ))^(-1)
        # = rotate(-θ), reflect(T), translation(-x,-y)
        self.ctx.rotate(-np.deg2rad(schematic.rotation))
        self.ctx.scale(-1 if schematic.reflected else 1, 1)
        self.ctx.translate(-schematic.pos[0], -schematic.pos[1])
                
class HTML_Canvas_Exporter(Exporter):
    def __init__(self, ctx):
        self.ctx = ctx
        self.canvas = ctx.canvas
        
        import js
        
        self.js = js
    
    def draw_line(self, line):
        
        self.ctx.beginPath()
        # self.ctx.lineWidth = line.thickness
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
        
        self.ctx.beginPath()
        self.ctx.ellipse(*arc.center, *arc.size, 0, *arc.theta_span) # TODO: rotation is 0 here
        self.ctx.stroke()
        
        # self.ctx.restore()
        
    def add_text(self, text_object):
        
        self.ctx.fillStyle = text_object.color().hex()
        
        self.ctx.font = str(text_object.font_size) + 'pt sans-serif';#text_object.font
        self.ctx.fillText(text_object.text, *text_object.get_pos("left"))
        
    def add_flag(self, flag):
        
        if isinstance(flag, Ground):
            print("GROUND")
            
    def draw(self, *args, **kwargs):
        self.ctx.lineWidth = self.js.thickness_slider.slider("get value")
        
        super().draw(*args, **kwargs)
    
    
class tikz_Exporter(Exporter):
    pass