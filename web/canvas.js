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

canvas.addEventListener('mousedown', onMouseDown);
canvas.addEventListener('mousemove', onMouseMove);
canvas.addEventListener('mouseup', onMouseUp);
canvas.addEventListener('wheel', onWheel);

window.addEventListener('load',   setupCanvas);
window.addEventListener('resize', setupCanvas);