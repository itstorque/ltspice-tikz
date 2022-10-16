from js import document, FileReader
from pyodide import create_proxy

from file_interface import parser
from exporter import HTML_Canvas_Exporter

canvas = document.getElementById("canvas")
ctx = canvas.getContext("2d")
CANVAS = HTML_Canvas_Exporter(ctx)

def set_running():
	document.getElementById("status").innerHTML = 'Python loaded and running ...'
 
def read_complete(event):
    # event is ProgressEvent

    content = document.getElementById("content")
    content.innerText = event.target.result

    schematic = parser(event.target.result)
    
    CANVAS.draw(schematic)

def redraw(event):
    # TODO: make this more efficient by caching schematic
    CANVAS.draw(parser(document.getElementById("content").innerText))

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