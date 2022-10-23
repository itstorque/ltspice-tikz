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
        # can add a component in here using either:
        #   schematic.add( Line.from_ltspice_gui_command(self.args) )
        # OR
        #   Line.add_to_parent_from_ltspice_gui_command(schematic, self.args)
        
        match self.command:
            
            case CMD.LINE:
                Line.add_to_parent_from_ltspice_gui_command(schematic, self.args)
            case CMD.RECTANGLE:
                Rectangle.add_to_parent_from_ltspice_gui_command(schematic, self.args)
            case CMD.ARC:
                Arc.add_to_parent_from_ltspice_gui_command(schematic, self.args)
            case CMD.CIRCLE:
                Circle.add_to_parent_from_ltspice_gui_command(schematic, self.args)
                
            case CMD.TEXT:
                Text.add_to_parent_from_ltspice_gui_command(schematic, self.args)
                
            case CMD.WIRE:
                Wire.add_to_parent_from_ltspice_gui_command(schematic, self.args)
            case CMD.SYMBOL:
                Symbol.add_to_parent_from_ltspice_gui_command(schematic, self.args)
                
                
            case CMD.FLAG:
                Flag.add_to_parent_from_ltspice_gui_command(schematic, self.args)
            
            case CMD.SYMATTR:
                pass # TODO: implement things that rely on last_symbol
                
            case _:
                pass # raise NotImplemented

def parser(raw, symbolstash):
    
    c = CircuitSchematic(symbolstash=symbolstash)
    
    last_symbol = None
    
    raw = raw.replace("\x00", "")
    
    for cmd in raw.split("\n")[1:]:
        
        cmd = " ".join(cmd.split())
        
        if cmd != "":
        
            cmd = Command(cmd)
            
            last_symbol = cmd(c, last_symbol)
            
    return c