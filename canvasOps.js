var c = document.getElementById('canvas');
var b1 = document.getElementById('cleario');
var endedq = 0;
//var eln = document.getElementById('endline')
//var cor = document.getElementById('corner');
//var randomrect = document.getElementById('rr');
//var resize = document.getElementById('size');
var ctx = c.getContext('2d');
var rect = c.getBoundingClientRect();
var isDrawing,points = [ ];

ctx.lineWidth = 4;
ctx.lineJoin = ctx.lineCap = 'round';

c.addEventListener('mousedown', function(evt){
  if(endedq == 0)
  {
    isDrawing = true;

    ctx.moveTo(
      parseInt(evt.clientX - rect.left), parseInt(evt.clientY - rect.top)
    );
  }
  else
  {
    if(endedq == 1)
    {
      xloc = parseInt(evt.clientX - rect.left);
      yloc = parseInt(evt.clientY - rect.top);
    }

    //given an array of xy coords and dsum
    /*if(cdatax.indexOf(xloc) == null && checkWithinRadius(xloc, yloc, temp,temp) == true)
    {
      console.log("works");
    }
    else
    {
      console.log("out of range");
    }*/
  }
}, false);
c.addEventListener('mousemove', function(evt) {
  if (isDrawing & endedq == 0) 
  {
    ctx.lineTo(
      parseInt(evt.clientX - rect.left),
      parseInt(evt.clientY - rect.top)
    );
    ctx.stroke();
  }
}, false);

c.onmouseup = function() {
  isDrawing = false;
};
//This clear the canvas
/*b1.onclick = function() 
{
ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
  isDrawing = false;
  ctx.beginPath();
};

eln.onclick = function()
{
  isDrawing = false;
  endedq = 1;
}




randomrect.onclick = function()
{
  ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
  isDrawing = false;
  ctx.beginPath();
  isDrawing = false;
  endedq = 1;
  randomRectangles(c,5);
}


//Random rectangles
function randomRectangles(canvas,nRectangles){
/// Draws `nRectangles` rectangles randomly placed and colored on `canvas`.
    var r,g,b,x,y,w,h,i;
    var context = canvas.getContext('2d');
    for( i=0; i<nRectangles; i+=1 ){
        r = Math.round(Math.random()*255);
        g = Math.round(Math.random()*255);
        b = Math.round(Math.random()*255);
        context.fillStyle = 'rgb('+r+','+g+','+b+')';
        x = Math.floor(Math.random()*canvas.width);
        w = Math.floor(Math.random()*canvas.width);
        y = Math.floor(Math.random()*canvas.height);
        h = Math.floor(Math.random()*canvas.height);
        context.fillRect(x,y,w,h);
    }
}

function outputUpdate(input) 
{
  document.querySelector('#pensize').value = input;
  ctx.beginPath();
  ctx.lineWidth = input;
  
}*/