# from browser import document, alert

# def click(ev):
#     alert(document["zone"].value)

# # bind event 'click' on button to function echo
# document["echo"].bind("click", click)

from browser import bind, window, document

load_btn = document["file_source"]
tikz_btn = document["to_tikz"]
copy_btn = document["copy"]

@bind(load_btn, "input")
def file_read(ev):

    def onload(event):
        """Triggered when file is read. The FileReader instance is
        event.target.
        The file content, as text, is the FileReader instance's "result"
        attribute."""
        document['file_text'].value = event.target.result
        
        draw_file(None)

    # Get the selected file as a DOM File object
    file = load_btn.files[0]
    # Create a new DOM FileReader instance
    reader = window.FileReader.new()
    # Read the file content as text
    reader.readAsText(file)
    reader.bind("load", onload)
    
@bind(tikz_btn, "click")
def draw_file(ev):
    
    data = document['file_text'].value
    
    
    
    document['output'].value = data