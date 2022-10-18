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
        # reader is a pyodide.JsProxy
        reader = FileReader.new()

        # Create a Python proxy for the callback function
        onload_event = create_proxy(read_complete)

        #console.log("done")

        reader.onload = onload_event

        reader.readAsText(f)

        return

def alert_method(title, msg):
    print("-----", title, "-----", msg)

def main():
    
    set_running()
    # Create a Python proxy for the callback function
    file_event = create_proxy(process_file)
    redraw_event = create_proxy(redraw)

    # Set the listener to the callback
    e = document.getElementById("file-upload")
    e.addEventListener("change", file_event, False)
    
    canvas.addEventListener("redraw", redraw_event, False)

main()