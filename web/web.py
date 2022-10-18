from js import document, FileReader, localStorage
from pyodide import create_proxy

from file_interface import parser
from exporter import HTML_Canvas_Exporter
from symbols import WebSymbolStash

canvas = document.getElementById("canvas")
ctx = canvas.getContext("2d")
CANVAS = HTML_Canvas_Exporter(ctx)

document.schematic = None

def set_running():
	document.getElementById("status").innerHTML = 'Python loaded and running ...'
 
def read_complete(event):
    # event is ProgressEvent

    content = document.getElementById("content")
    content.innerText = event.target.result
    
    document.schematic = parser(event.target.result, symbolstash=WebSymbolStash(localStorage, "symbols", alert_method))
    
    redraw(None)

def redraw(event):
    # TODO: make this more efficient by caching schematic
    
    canvas =  document.getElementById("canvas")
    ctx = canvas.getContext("2d")
    
    ctx.save()
    ctx.setTransform(1,0,0,1,0,0)
    ctx.clearRect(0, 0, canvas.width, canvas.height)
    ctx.restore()
    
    if document.schematic:
        CANVAS.draw(document.schematic)

async def process_file(x):
    fileList = document.getElementById('file-upload').files

    for f in fileList:

        reader = FileReader.new()

        onload_event = create_proxy(read_complete)

        reader.onload = onload_event

        reader.readAsText(f)

        return

def alert_method(title, msg):
    print("-----", title, "-----", msg)

def add_symbol_from_source(event):
    stash = WebSymbolStash(localStorage, "symbols", alert_method)
    stash.add(event.target.filename.replace(".asy", ""), event.target.result)

def add_symbols(event):
    fileList = document.getElementById('symbol-upload').files
    
    for f in fileList:
        
        reader = FileReader.new()
        
        onload_event = create_proxy(add_symbol_from_source)
        
        reader.filename = f.name
        
        reader.onload = onload_event
        
        reader.readAsText(f)

def main():
    
    set_running()
    # Create a Python proxy for the callback function
    file_event = create_proxy(process_file)
    symbol_event = create_proxy(add_symbols)
    redraw_event = create_proxy(redraw)

    # Set the listener to the callback
    e = document.getElementById("file-upload")
    e.addEventListener("change", file_event, False)
    
    e = document.getElementById("symbol-upload")
    e.addEventListener("change", symbol_event, False)
    
    canvas.addEventListener("redraw", redraw_event, False)

main()