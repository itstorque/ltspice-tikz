import glob, os
import sys
import numpy as np

coord = lambda x: np.floor(float(x)/50*100)/100

WIRES = {}

tikzset_defs = set()
TIKZSET = """\\tikzset{
    partial ellipse/.style args={#1:#2:#3}{
        insert path={+ (#1:#3) arc (#1:#2:#3)}
    }
}"""
TIKZCODE = ""

unitvec = lambda vec: vec / np.linalg.norm(vec)

angle = lambda v: np.degrees(np.arctan2(v[1], v[0]))

def tikz_add(s):
    
    global TIKZCODE
    
    TIKZCODE += s + "\n"
    
def add_symbol(symfile):
    
    global TIKZSET
    
    tikzset_defs.add(symfile)
    
#     \tikzset{ pics/res.asy/.style args={#1/#2}{
# code={
# \draw (0.32,1.76) to (0.32,1.92);\draw (0.0,1.6) to (0.32,1.76);\draw (0.64,1.28) to (0.0,1.6);\draw (0.0,0.96) to (0.64,1.28);\draw (0.64,0.64) to (0.0,0.96);\draw (0.32,0.32) to (0.32,0.48);\draw (0.32,0.48) to (0.64,0.64);\draw (0.72,0.8) node {#1};\draw (0.72,1.52) node {#2};
# }
# }
# }

    with open(symfile, "r") as f:
        
        TIKZSET += "\\tikzset{ pics/" + symfile + "/.style args={#1*^*#2}{code={"
        
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
                
                coords = np.array([coord(i) for i in cmd[2:10]])
                
                pos = coords[0:2]
                
                size = abs(pos - coords[2:4])/2
                
                center = (pos + coords[2:4])/2
                
                theta_i = angle(coords[6:8]-center)
                theta_f = angle(coords[4:6]-center)
                
                TIKZSET += f"\draw ({center[0]},{center[1]}) [partial ellipse={theta_i}:{theta_f}:{size[0]} and {size[1]}];"
                
            elif cmd[0] == "WINDOW":
                
                # WINDOW 0 24 16 Left 2
                # WINDOW 1 36 80 Left 2
                
                print("WOOT")
                
                type = cmd[1]
                pos = [coord(i) for i in cmd[2:4]]
                
                alignment = cmd[4]
                fontsize = cmd[5]
                
                text = ""
                
                if type=="0": 
                    text = "#1"
                elif type=="3": 
                    text = "#2"
                
                TIKZSET += f"\\draw ({pos[0]},{pos[1]}) node[yscale=-1] {{{text}}};"
                
        TIKZSET += "}}}"

def draw_symbol(symfile, loc, angle, data0, data3):
    
    global TIKZCODE
    
    if symfile in tikzset_defs:
        # place in circ
        pass
    else:
        add_symbol(symfile)
        
            
    TIKZCODE += f"\path[rotate around ={'{'}{angle}:({loc[0]}, {loc[1]}){'}'}, anchor=west, transform shape] ({loc[0]}, {loc[1]}) pic{{{symfile}={data0}*^*{data3}}};"
    
def parse_circuit(circuit):
    
    global TIKZCODE
    
    circuit_split = circuit.split("\n")
    
    k=-1
    for i in circuit_split:
        
        k+=1
        
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
                draw_symbol("gnd.asy", coords, 0, "", "")
            
            # print(f"({coords[0]},{coords[1]}) to ({coords[0]},{coords[1]}) {node_type}")
            
        elif "SYMBOL" in cmd[0]:

            os.chdir("/Users/torque/Library/Application Support/LTspice/lib/sym")
            
            coords = [coord(i) for i in cmd[2:4]]
            
            angle = int(cmd[4][1:])
            
            symfile = glob.glob(cmd[1].lower()+".asy")[0]
            
            klocal = 0
            
            data0 = ""
            data3 = ""
            
            while klocal<100:
                klocal+=1
                
                cmd = circuit_split[k+klocal].split(" ")
                
                if cmd[0]=="SYMATTR":
                    if cmd[1] == "InstName": data0 = cmd[2]
                    elif cmd[1] == "Value": data3 = cmd[2]
                elif cmd[0] not in {"WINDOW"}:
                    break
            
            draw_symbol(symfile, coords, angle, data0, data3)
            
            # if "Voltage" in cmd[1]:
                
            #     print(f"({coords[0]},{coords[1]}) to [V,v<=$V_1$,rotate={angle}] ({coords[0]},{coords[1]})")
            
    tikz_add(";")

def circ_to_latex(circuit):
    
    res = ""
    
    parse_circuit(circuit)

    res += "\documentclass[tikz,border=2mm]{standalone}\n"
    res += TIKZSET
    res += """\n\\begin{document}
    \\begin{tikzpicture}[yscale = -1]\n"""
    res += TIKZCODE
    res+="""\n
    \end{tikzpicture}
    \end{document}"""
    
    return res

def detect_encoding(file_path, expected_str: str = '') -> str:
    """
    Simple strategy to detect file encoding.  If an expected_str is given the function will scan through the possible
    encodings and return a match.
    If an expected string is not given, it will use the second character is null, high chances are that this file has an
    'utf_16_le' encoding, otherwise it is assuming that it is 'utf-8'.
    :param file_path: path to the filename
    :type file_path: str
    :param expected_str: text which the file should start with
    :type expected_str: str
    :return: detected encoding
    :rtype: str
    """
    for encoding in ('utf-8', 'utf_16_le', 'cp1252', 'cp1250', 'shift-jis'):
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                lines = f.readlines()
                f.seek(0)
        except UnicodeDecodeError:
            # This encoding didn't work, let's try again
            continue
        else:
            if expected_str:
                if not lines[0].startswith(expected_str):
                    # File did not start with expected string
                    # Try again with a different encoding (This is unlikely to resolve the issue)
                    continue
            if encoding == 'utf-8' and lines[0][1] == '\x00':
                continue
            return encoding
    else:
        raise UnicodeError("Unable to detect log file encoding")

add_symbol("gnd.asy")

def open_file(file):
    
    with open(file, "rb") as f:
        return decode_data(f.read())

def decode_data(data):
    
    return data.decode(detect_encoding(sys.argv[1], "Version"))
    
    # data = data.replace(b'\x00', b'')
    
    try:
        circuit = data.decode('utf-16-le')
        print(circuit)
    except:
        try:
            circuit = data[1:].decode('utf-8')
        except:
            circuit = data[2:].decode('utf-8')
            
    return circuit

# def try_to_read(file):

if __name__=="__main__":
    
    try:
        import pyperclip
        clipboard = True
    except:
        clipboard = False
        print("If you want the result copied to your clipboard, run [pip install pyperclip]")

    circuit = open_file(sys.argv[1])

    res = circ_to_latex(circuit)
    
    if clipboard:
        pyperclip.copy(res)
        print("latex code copied to clipboard")
        
    else:
        print("\n\n\n", res)