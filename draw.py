import glob, os
import numpy as np

coord = lambda x: np.floor(float(x)/50*100)/100

WIRES = {}

tikzset_defs = set()
TIKZSET = ""
TIKZCODE = ""

def tikz_add(s):
    
    global TIKZCODE
    
    TIKZCODE += s + "\n"
    
def add_symbol(symfile):
    
    global TIKZSET
    
    tikzset_defs.add(symfile)

    with open(symfile, "r") as f:
        
        # print(f";\n\\begin{{scope}}[rotate={angle}]\n \\draw ")
        
        TIKZSET += "\\tikzset{ {" + symfile + "}/.pic = {"
        
        for i in f.read().split("\n"):
            
            cmd = i.split(" ")
            
            if cmd[0] == "LINE":
                
                coords = [coord(i) for i in cmd[2:6]]
                
                style = cmd[1]
                
                TIKZSET += f"\draw ({coords[0]},{coords[1]}) to ({coords[2]},{coords[3]});"
                
            elif cmd[0] == "CIRCLE":
                
                coords = [coord(i) for i in cmd[2:6]]
                
                style = cmd[1]
                
                pos = np.array(coords[0:2])
                size = abs(pos - coords[2:4])/2
                
                pos += size
                
                TIKZSET += f"\draw ({pos[0]},{pos[1]}) ellipse ({size[0]} and {size[1]});"
                
            elif cmd[0] == "ARC":
                
                coords = [coord(i) for i in cmd[2:6]]
                
        TIKZSET += "}}"

def draw_symbol(symfile, loc, angle):
    
    global TIKZCODE
    
    if symfile in tikzset_defs:
        # place in circ
        pass
    else:
        add_symbol(symfile)
        
            
    TIKZCODE += f"\path[rotate around ={'{'}{angle}:({loc[0]}, {loc[1]}){'}'}, anchor=west, transform shape] ({loc[0]}, {loc[1]}) pic{{{symfile}}};"
    
def parse_circuit(circuit):
    
    global TIKZCODE
    
    for i in circuit.split("\n"):
        
        cmd = i.split(" ")
        
        if "WIRE" in cmd[0]:
            
            # print(i)
            
            coords = [coord(i) for i in cmd[1:5]]
            
            tikz_add(f"\\draw ({coords[0]},{coords[1]}) to ({coords[2]},{coords[3]});")
            
            WIRES[(coords[0],coords[1])] = (coords[2],coords[3])
            WIRES[(coords[2],coords[3])] = (coords[0],coords[1])
            
        elif "FLAG" in cmd[0]:
            
            # tikz_add("%" + i)
            
            coords = [coord(i) for i in cmd[1:3]]
            
            node_type = cmd[3]
            
            if node_type == "0":
                draw_symbol("gnd.asy", coords, 0)
            
            # print(f"({coords[0]},{coords[1]}) to ({coords[0]},{coords[1]}) {node_type}")
            
        elif "SYMBOL" in cmd[0]:

            os.chdir("/Users/torque/Library/Application Support/LTspice/lib/sym")
            
            coords = [coord(i) for i in cmd[2:4]]
            
            angle = int(cmd[4][1:])
            
            symfile = glob.glob("" + cmd[1].lower()+".asy")[0]
            
            draw_symbol(symfile, coords, angle)
            
            # if "Voltage" in cmd[1]:
                
            #     print(f"({coords[0]},{coords[1]}) to [V,v<=$V_1$,rotate={angle}] ({coords[0]},{coords[1]})")
            
    tikz_add(";")

add_symbol("gnd.asy")
    
circuit = None

with open("test.asc", "rb") as f:
    data = f.read()
    data = data.replace(b'\x00', b'')
    data = data[2:]
    
    circuit = data.decode('utf-8')

parse_circuit(circuit)

print("""\documentclass[tikz,border=2mm]{standalone}""")
print(TIKZSET)
print("""\\begin{document}
\\begin{tikzpicture}[yscale = -1]""")
print(TIKZCODE)
print("""
\end{tikzpicture}
\end{document}
      """)