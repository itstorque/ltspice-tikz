const redraw = new Event('redraw');

const canvas = document.getElementById('canvas');
const context = canvas.getContext('2d');

context.imageSmoothingEnabled = false;
scale = 2

let isDragging = false;
let dragStartPosition = { x: 0, y: 0 };
let currentTransformedCursor;

let transformProperties = null;

function setupCanvas(event) {

    canvas.width  = window.innerWidth * scale;
    canvas.height = window.innerHeight * scale;

    if (transformProperties == null) {
        transformProperties = canvas.getTransform();
    }

    context.setTransform(transformProperties);

    render();
}

function render() {
    canvas.dispatchEvent(redraw);
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

    currentTransformedCursor = getTransformedPoint(event.offsetX, event.offsetY)

    if (isDragging) {
        context.translate(currentTransformedCursor.x - dragStartPosition.x, currentTransformedCursor.y - dragStartPosition.y);
        render();
    }
    
    transformProperties = context.getTransform();

}

function onMouseUp() {
	isDragging = false;
}

function onWheel(event) {

    const zoom = event.deltaY < 0 ? 1.1 : 0.9;
  
    context.translate(currentTransformedCursor.x, currentTransformedCursor.y);
    context.scale(zoom, zoom);
    context.translate(-currentTransformedCursor.x, -currentTransformedCursor.y);

    transformProperties = context.getTransform();
        
    render();
    event.preventDefault();

}

function missing_symbol_error() {
    $("#missing_symbol").modal("show");
}

function toColorObject() {
    return $("#to_color_dropdown").dropdown("get value")
}

canvas.addEventListener('mousedown', onMouseDown);
canvas.addEventListener('mousemove', onMouseMove);
canvas.addEventListener('mouseup', onMouseUp);
canvas.addEventListener('wheel', onWheel);

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
        value: 'background'
      },
      {
        name: 'Components',
        value: 'components'
      },
      {
        name: 'Wires',
        value: 'wires'
      },
      {
        name: 'Flags',
        value: 'flags'
      },
      {
        name: 'Text',
        value: 'text'
      },
      {
        name: 'Comments',
        value: 'comments'
      },
      {
        name: 'Commands',
        value: 'Commands'
      }
    ]
  })
;