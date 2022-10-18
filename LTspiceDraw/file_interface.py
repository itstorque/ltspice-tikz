from circuit import *
from geometry import *

from enum import Enum
from pathlib import Path

class CMD(Enum):
    
    WIRE = "WIRE"
    FLAG = "FLAG"
    
    SYMBOL = "SYMBOL"
    SYMATTR = "SYMATTR"
    SYMBOLTYPE = "SYMBOLTYPE"
    PIN = "PIN" # TODO: add a way of visualizing PINS?
    PINATTR = "PINATTR"
    
    WINDOW = "WINDOW"
    SHEET = "SHEET"
    
    LINE = "LINE"
    RECTANGLE = "RECTANGLE"
    ARC = "ARC"
    CIRCLE = "CIRCLE"
    TEXT = "TEXT"
    
class Command:
    
    def __init__(self, cmd):
        
        cmd = cmd.split(" ")
        
        self.command = CMD(cmd[0].upper())
        self.args = cmd[1:]
        
    def __str__(self):
        return self.command.value + " < " + str(self.args)
    
    def __call__(self, schematic, last_symbol=None):
        
        match self.command:
            
            case CMD.LINE:
                schematic.add( Line.from_ltspice_gui_command(self.args) )
            case CMD.RECTANGLE:
                schematic.add( Rectangle.from_ltspice_gui_command(self.args) )
            case CMD.ARC:
                schematic.add( Arc.from_ltspice_gui_command(self.args) )
            case CMD.CIRCLE:
                schematic.add( Circle.from_ltspice_gui_command(self.args) )
                
            case CMD.TEXT:
                # schematic.add( Text.from_ltspice_gui_command(self.args) )
                pass #TODO: implement text object
                
            case CMD.WIRE:
                schematic.add( Wire.from_ltspice_gui_command(self.args) )
            case CMD.SYMBOL:
                symbol = Symbol.from_ltspice_gui_command(self.args)
                schematic.add( *symbol )
                return symbol
            
            case CMD.SYMATTR:
                pass # TODO: implement things that rely on last_symbol
                
            case _:
                pass # raise NotImplemented

def parser(raw):
    
    c = CircuitSchematic()
    
    last_symbol = None
    
    for cmd in raw.split("\n")[1:]:
        
        if cmd != "":
        
            cmd = Command(cmd)
            
            last_symbol = cmd(c, last_symbol)
            
    return c