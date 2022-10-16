# from geometry import *

# class TikzArc(Arc):
    
#     def __init__(self, arc) -> None:
#         super().__init__(arc.center, arc.size, arc.theta_span, arc.linestyle, arc.color)
        
#     def draw(self):
        
#         return f"\draw ({self.center[0]},{self.center[1]}) [partial ellipse={self.theta_span[0]}:{self.theta_span[1]}:{self.size[0]} and {self.size[1]}];\n"
    
# if __name__=="__main__":
    
#     TikzArc(Arc())