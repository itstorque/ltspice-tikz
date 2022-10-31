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
    
    def draw_inner_setup(self, elem):
        pass
    
    def draw(self, schematic, **kwargs):
        
        drawings_cache = set()
        
        for elem in schematic.geometries:
            
            elem.color().fallback(schematic.color())
            
            self.draw_inner_setup(elem)
            
            if type(elem) == Line:
                drawings_cache.add( self.draw_line(elem) )
                
            elif type(elem) == Circle:
                drawings_cache.add( self.draw_circle(elem) )
                
            elif type(elem) == Arc:
                drawings_cache.add( self.draw_arc(elem) )
                
            elif type(elem) == Rectangle:
                drawings_cache.add( self.draw_rectangle(elem) )
                
            elif type(elem) == Text:
                elem.color().fallback(schematic.textColor(elem.type))
                drawings_cache.add( self.add_text(elem) )
                
            elif type(elem) == Ground:
                drawings_cache = drawings_cache.union( self.draw(elem, **kwargs) )
                
            elif type(elem) == Flag:
                drawings_cache = drawings_cache.union( self.draw(elem, **kwargs) )
                
            elif type(elem) == Symbol:
                # elem.color().fallback(schematic.textColor(elem.type))
                drawings_cache = drawings_cache.union( self.draw(elem, **kwargs) )
                
        return drawings_cache
                
class HTML_Canvas_Exporter(Exporter):
    def __init__(self, ctx):
        super().__init__()
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
        
        return line
    
    def draw_rectangle(self, rectangle):
        
        self.ctx.beginPath()
        self.ctx.rect(*rectangle.start, *rectangle.end)
        self.ctx.stroke()
        
        return rectangle
    
    def draw_circle(self, circle):
        
        self.ctx.beginPath()
        self.ctx.arc(*circle.center, circle.size[0], 0, 2 * np.pi)
        self.ctx.stroke()
        
        # self.draw_arc(circle)
        
        return circle
        
    def draw_arc(self, arc):
        
        self.ctx.beginPath()
        self.ctx.ellipse(*arc.center, *arc.size, 0, *arc.theta_span) # TODO: rotation is 0 here
        self.ctx.stroke()
        
        # self.ctx.restore()
        
        return arc
        
    def add_text(self, text_object):
        
        self.ctx.fillStyle = text_object.color().hex()
        
        self.ctx.font = str(text_object.font_size) + 'pt sans-serif';#text_object.font
        self.ctx.fillText(text_object.text, *text_object.get_pos("left"))
        
        return text_object
    
    def draw_inner_setup(self, elem):
        self.ctx.strokeStyle = elem.color().hex()
            
    def draw(self, schematic, *args, **kwargs):
        
        if schematic.backgroundColor:
            # self.ctx.fillStyle = schematic.backgroundColor;
            # self.ctx.fillRect(0, 0, self.canvas.width, self.canvas.height);
            self.canvas.style.backgroundColor = schematic.backgroundColor().hex()
        
        # TODO: move these to only be in the HTML_canvas_exporter class
        
        # apply transformation into the frame of reference of the component
        self.ctx.translate(*schematic.pos)
        self.ctx.scale(-1 if schematic.reflected else 1, 1)
        self.ctx.rotate(np.deg2rad(schematic.rotation))
        
        self.ctx.lineWidth = self.js.thickness_slider.slider("get value")
        
        out = super().draw(schematic, *args, **kwargs)
               
        # apply inverse of transformation done before drawing 
        # Order matters... Since we applied translation(x,y), reflect(T), rotate(θ)
        # we need to apply (translation(x,y), reflect(T), rotate(θ))^(-1)
        # = rotate(-θ), reflect(T), translation(-x,-y)
        self.ctx.rotate(-np.deg2rad(schematic.rotation))
        self.ctx.scale(-1 if schematic.reflected else 1, 1)
        self.ctx.translate(-schematic.pos[0], -schematic.pos[1])
        
        return out
    
    
class Tikz_Exporter(Exporter):
    
    def __init__(self):
        super().__init__()
    
    def draw_line(self, line):
        return f"\draw ({line.start[0]},{line.start[1]}) to ({line.end[0]},{line.end[1]});"
    
    def draw_rectangle(self, rectangle):
        raise NotImplementedError
    
    def draw_circle(self, circle):
        return f"\draw ({circle.center[0]},{circle.center[1]}) ellipse ({circle.size[0]} and {circle.size[1]});"
        
    def draw_arc(self, arc):
        return f"\draw ({arc.center[0]},{arc.center[1]}) [partial ellipse={arc.theta_span[0]}:{arc.theta_span[1]}:{arc.size[0]} and {arc.size[1]}];"
        
    def add_text(self, text_object):
        pass # TODO: not implemented yet...
        return f""
    
    def draw(self, schematic, _main_call=True):
        
        if _main_call:
            return '\n'.join(super().draw(schematic, _main_call=False))
        return super().draw(schematic, _main_call=False)