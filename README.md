# LTspice Tikz

This program converts LTspice schematics and symbols (`.asc` or `.asy` 
files) into LaTeX Tikz code. This package draws each symbol in the 
schematic from its original symbol removing the need to create your own
representation of each element for a drawing program.

To use it, run `python draw.py [file-to-convert-here]`, the LaTeX code
will be copied into your clipboard if you have pyperclip installed,
otherwise it will print out the output into your terminal.

## TODO

- better search for symbol files
- dashed and dotted support
- test script to make sure this works
- orientation of gnd
- actual support of flags
- general text support
- tran command support?
- types of export
- documentation
- a nice command/integration into spice-daemon
- plot size choice