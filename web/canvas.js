const redraw = new Event('redraw');
const ui_click = new Event('ui_click');

const canvas = document.getElementById('canvas');
const context = canvas.getContext('2d');

const tooltips_canvas = document.getElementById('tooltips_canvas');
const tooltips_context = tooltips_canvas.getContext('2d');

const tooltip_color = "#2E8EC8";

let in_edit_mode = false;

controlling_canvas = tooltips_canvas

context.imageSmoothingEnabled = false;
scale = 2

let isDragging = false;
let didDragBy = false;

let element_selected = Object();

let total_zoom = 1;

let dragStartPosition = { x: 0, y: 0 };
let currentTransformedCursor;

let transformProperties = null;

currentTransformedCursor = getTransformedPoint(0, 0)

function setupCanvas(event) {

    canvas.width  = window.innerWidth * scale;
    canvas.height = window.innerHeight * scale;

    tooltips_canvas.width  = canvas.width;
    tooltips_canvas.height = canvas.height;

    if (transformProperties == null) {
        transformProperties = canvas.getTransform();
    }

    context.setTransform(transformProperties);
    tooltips_context.setTransform(transformProperties);

    render();
}

function render() {
    canvas.dispatchEvent(redraw);
    if (in_edit_mode) { tooltip_redraw(); }
}

function onMouseDown(event) {

    isDragging = true;
    dragStartPosition = getTransformedPoint(event.offsetX, event.offsetY);

}

function getTransformedPoint(x, y) {

    const originalPoint = new DOMPoint(x*scale, y*scale);

    return context.getTransform().invertSelf().transformPoint(originalPoint);

}

function onMouseMove(event) {

    if (isDragging) {

        currentTransformedCursor = getTransformedPoint(event.offsetX, event.offsetY)

        deltaX = currentTransformedCursor.x - dragStartPosition.x;
        deltaY = currentTransformedCursor.y - dragStartPosition.y;

        didDragBy += Math.abs(deltaX)
        didDragBy += Math.abs(deltaY)

        context.translate(deltaX, deltaY);

        tooltips_context.setTransform(context.getTransform());

        render();
    
        transformProperties = context.getTransform();

    }

}

function onMouseUp(event) {

    if (didDragBy < 5) {

        currentTransformedCursor = getTransformedPoint(event.offsetX, event.offsetY);

        if (in_edit_mode) {

            // response = ui_click(currentTransformedCursor.x, currentTransformedCursor.y);

            // console.log(response);
            // console.log(ui_click);

            // element_selected = response;

            // tooltip_redraw(event);

            ui_click.x = currentTransformedCursor.x
            ui_click.y = currentTransformedCursor.y

            tooltips_canvas.dispatchEvent(ui_click);

        }

    }
    
	isDragging = false;
    didDragBy = 0;

}

function onWheel(event) {

    const zoom = event.deltaY < 0 ? 1.08 : 0.92;

    total_zoom *= zoom;
  
    context.translate(currentTransformedCursor.x, currentTransformedCursor.y);
    context.scale(zoom, zoom);
    context.translate(-currentTransformedCursor.x, -currentTransformedCursor.y);

    transformProperties = context.getTransform();
    tooltips_context.setTransform(transformProperties);
        
    render();
    event.preventDefault();

}

function missing_symbol_error() {
    $("#missing_symbol").modal("show");
}

function toColorObject() {
    return $("#to_color_dropdown").dropdown("get value")
}

function toggle_edit_mode() {
    in_edit_mode = !in_edit_mode;
    $("#edit_schematic_button").toggleClass("active");
}

function draw_selected_elem_bounding_box(element_selected) {

    tooltips_context.strokeStyle = "#000";
    tooltips_context.beginPath();
    tooltips_context.setLineDash([12/total_zoom]);
    tooltips_context.lineWidth = 3/total_zoom;
    tooltips_context.rect(element_selected.x, element_selected.y, element_selected.x2 - element_selected.x, element_selected.y2 - element_selected.y); 
    tooltips_context.stroke();
    tooltips_context.setLineDash([]);

    const s = 6; 

    tooltips_context.fillStyle = tooltip_color;
    tooltips_context.fillRect(element_selected.x-s/total_zoom, element_selected.y-s/total_zoom, 2*s/total_zoom, 2*s/total_zoom)
    tooltips_context.fillRect(element_selected.x2-s/total_zoom, element_selected.y-s/total_zoom, 2*s/total_zoom, 2*s/total_zoom)
    tooltips_context.fillRect(element_selected.x-s/total_zoom, element_selected.y2-s/total_zoom, 2*s/total_zoom, 2*s/total_zoom)
    tooltips_context.fillRect(element_selected.x2-s/total_zoom, element_selected.y2-s/total_zoom, 2*s/total_zoom, 2*s/total_zoom)

}

function tooltip_redraw(event) {

    tooltips_context.save()
    tooltips_context.setTransform(1,0,0,1,0,0)
    tooltips_context.clearRect(0, 0, canvas.width, canvas.height)
    tooltips_context.restore()

    if (document.element_selected) {
        
        element_selected.x = document.element_selected.get("x")
        element_selected.y = document.element_selected.get("y")
        element_selected.x2 = document.element_selected.get("x2")
        element_selected.y2 = document.element_selected.get("y2")
        
        draw_selected_elem_bounding_box(element_selected)

    }

}

controlling_canvas.addEventListener('mousedown', onMouseDown);
controlling_canvas.addEventListener('mousemove', onMouseMove);
controlling_canvas.addEventListener('mouseup', onMouseUp);
controlling_canvas.addEventListener('wheel', onWheel);

window.addEventListener('load',   setupCanvas);
window.addEventListener('resize', setupCanvas);

var colorPicker = new iro.ColorPicker('#picker', {
    // color picker options
    // Option guide: https://iro.js.org/guide.html#color-picker-options
    width: 190,
    color: "rgb(0, 0, 0)",
    borderWidth: 1,
    borderColor: "#fff",
    layout: [
        {
          component: iro.ui.Box,
        },
        {
          component: iro.ui.Slider,
          options: {
            id: 'hue-slider',
            sliderType: 'hue'
          }
        }
      ]
  });

colorPicker.on('color:change', function(color) {
    // log the current color as a HEX string
    render();
});

var swatchGrid = document.getElementById('swatch-grid');

swatchGrid.addEventListener('click', function(e) {
  var clickTarget = e.target;
  // read data-color attribute
  if (clickTarget.dataset.color) {
    // update the color picker
    colorPicker.color.set(clickTarget.dataset.color);
  }
});

$('#styling_button')
  .popup({
    popup : $('#styling_popup'),
    inline: true,
    on: "click"
  })
;

$('#source_code_button')
  .popup({
    popup : $('#source_code'),
    inline: true,
    on: "click"
  })
;

$('#to_color_dropdown')
  .dropdown({
    values: [
      {
        name: 'Schematic',
        value: 'schematic',
        selected: true
      },
      {
        name: 'Background',
        value: 'background',
        selected: false
      },
      {
        name: 'Components',
        value: 'components',
        selected: false
      },
      {
        name: 'Wires',
        value: 'wires',
        selected: false
      },
      {
        name: 'Flags',
        value: 'flags',
        selected: false
      },
      {
        name: 'Text',
        value: 'text',
        selected: false
      },
      {
        name: 'Comments',
        value: 'comments',
        selected: false
      },
      {
        name: 'Commands',
        value: 'Commands',
        selected: false
      }
    ]
  })
;

thickness_slider = $('#line_thickness')

thickness_slider
  .slider({
    min: 0.1,
    max: 5,
    start: 2,
    step: 0.1,
    onChange: function(value) {
        render();
    }
  })
;

$("#edit_schematic_button").click(toggle_edit_mode);