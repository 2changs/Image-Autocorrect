	<head>
	  <link rel="stylesheet" type="text/css" href="stl.css">

	  <title>Image Auto Correct</title>
	</head>
	<body>
		<!-- <nav>
		 <div id = "colors">
		    <button type = "button" class = "color" id = "red"></button>
		    <button type = "button" class = "color" id = "orange"></button>
		    <button type = "button" class = "color" id = "yellow"></button>
		    <button type = "button" class = "color" id = "green"></button>
		    <button type = "button" class = "color" id = "blue"></button>
		    <button type = "button" class = "color" id = "purple"></button>
		    <button type = "button" class = "color" id = "brown"></button>
		    <button type = "button" class = "color" id = "black"></button>
		    <button type = "button" class = "color" id = "white"></button>
		    <button type = "button" class = "sa" id = "endline">End</button>
		    <button type = "button" class = "co" id = "corner">Check</button>
		    <button type = "button" class = "randrect" id = "rr">RanRec</button>
		  </div> 
		    <p>
		    <input type = "range" id = "size" min = "1" max = "40" step = "1" value = "10" onchange="outputUpdate(value)">
		      <output for=size id=pensize class = "otpt">10</output>
		  </p> 
		  <p>
		    <button type="button" class="btn" id = "cleario">Clear Canvas</button>
		  </p>

		</nav>-->
<!-- 		<div id = "holder"> </div>
		<div id = "toolbar">
			<button> Button </button>
		</div> -->
		<div id = "c1">
			<canvas id="canvas" ></canvas>
<!-- 			<div id="toolbar"> 

			  <button type="button" class="round-button" style="background-color: red; width: 50px; height:50px;"></button>
			  <button type="button" class="round-button" style="background-color: orange; width: 50px; height:50px;"></button>
			  <button type="button" class="round-button" style="background-color: yellow; width: 50px; height:50px;"></button>
			  <button type="button" class="round-button" style="background-color: green; width: 50px; height:50px;"></button>
			  <button type="button" class="round-button" style="background-color: blue; width: 50px; height:50px;"></button>
			  <button type="button" class="round-button" style="background-color: purple; width: 50px; height:50px;"></button>


			</div> -->
			<form name="form" id="form" action="canvas.php"  method="post"> 
				<input hidden id="array" value="" name="array" readonly> </input>
				<input hidden id="size"  value="" name="size" readonly> </input> 
				<input hidden type="submit"> </input>
			</form>

		</div>

	</body>

    <script src="//ajax.googleapis.com/ajax/libs/jquery/2.1.3/jquery.min.js"></script>
	<!--<script src="colorButton.js"></script> -->
	<script src="canvasOps.js"></script> 


<p id="p"> </p>

<?php 
	/*$file = fopen("shapes.txt", "r") or die("Unable to open file");
	$arr = fread($file, filesize("shapes.txt"));
	$shapes = explode(" ", $arr);
	echo $shapes;
	fclose($file);*/
	


	if(!empty($_POST["array"]))
	{
		$array = $_POST['array'];
		$size  = $_POST["size"];
		exec("python test.py $array $size", $output);

		for ($x = 0; $x <= count($output);  $x++) {
		    echo $output[$x];
		} 

		$shape = $output[0];
		$line = $output[1];
	}
	else{
		$array = "EMPTY";
	}

?>


<script>
var arrayOfPixels = [];
var prevArrayOfPixels = [];
var c = document.getElementById("canvas");
var context = c.getContext("2d");
var array = '<?php echo $o ?>';
var stringLine = '<?php echo $line ?>';
var shapeDetected = '<?php echo $shape ?>';
var shapesDrawn = '<?php echo $shapes ?>';
var points = [];
var tempPoint = "";
var clicked = false;
window.addEventListener('resize', resizeCanvas, false);
resizeCanvas();
createCanvasArray();
drawOldShapes();
createShape();
console.log(shapeDetected);


function resizeCanvas() {
    c.width = window.innerWidth;
    c.height = window.innerHeight;

}


function createShape(){
	//create array for line---------------------
	//if statements checking each shape
	if(shapeDetected == "Ellipse"){									//if it is an ellipse					
		createShapeArray();
		drawEllipse();
		//redraw();
	}

	if(shapeDetected == "Line"){									//if it is a line
		createShapeArray();
		drawLine();
		//redraw();
	}

	if(shapeDetected == "Rectangle"){
		createShapeArray();
		drawRectangle();
	}

	if(shapeDetected == "Rotated Rectangle"){
		createShapeArray();
		drawRotatedRectangle();
	}

	if(shapeDetected == "Triangle"){
		createShapeArray();
		drawTriangle();
	}
}

function drawOldShapes(){
	console.log(shapesDrawn[0]);




}


function createShapeArray(){
	for(var i = 0; i < stringLine.length; i++){
		if(stringLine[i] == " "){
				var point = parseFloat(tempPoint);
				points.push(point);
				tempPoint = "";
			}
			else{
				tempPoint+=stringLine[i];
			}
		}
	var point = parseFloat(tempPoint);
	points.push(point);


}

function createCanvasArray(){
	//create array for canvas-------------------
	var temp  = "";
	var num = 0; 
	if(array != "EMPTY"){
		for(var i = 0; i < array.length; i++){
			if(array[i] != ","){
				temp+=array[i];
			}
			else if(array[i] == ","){
				num = parseFloat(temp);
				prevArrayOfPixels.push(num);
				num = 0;
				temp="";
			}
		}
		num = parseFloat(temp); 
		prevArrayOfPixels.push(num);
		num = 0;
		temp="";
		//drawOldPic();
	}
	//-----------------------------------------
}

function drawLine(){
	context.moveTo(points[0],points[1]);
	context.lineTo(points[2],points[3]);
	context.lineWidth = 1;
	context.stroke(); 
	//var rtempline = defLine(points[0], points[1], points[2], points[3]);
	//shapeHolder.push(rtempline);
}

function drawEllipse(){
	centerX = points[0];
	centerY = points[1];
	radiusX = points[2]/2;
	radiusY = points[3]/2;
	rotationAngle = points[4]*Math.PI/180;
	console.log(points);

	for (var i = 0 * Math.PI; i < 2 * Math.PI; i += 0.01 ) {
	    xPos = centerX - (radiusX * Math.sin(i)) * Math.sin(rotationAngle * Math.PI) + (radiusY * Math.cos(i)) * Math.cos(rotationAngle * Math.PI);
	    yPos = centerY + (radiusY * Math.cos(i)) * Math.sin(rotationAngle * Math.PI) + (radiusX * Math.sin(i)) * Math.cos(rotationAngle * Math.PI);

	    if (i == 0) {
	        context.moveTo(xPos, yPos);
	    } else {
	        context.lineTo(xPos, yPos);
	    }
	}
	context.stroke();
}


function drawRectangle(){
	cornerx = points[0];
	cornery = points[1];
	width   = points[2];
	height  = points[3];

	context.beginPath();
    context.rect(cornerx, cornery, height, width);
    context.strokeStyle = 'black';
    context.stroke();
}

function drawTriangle(){
	console.log("drawing triangle");
	cornerOneX = points[0];
	cornerOneY = points[1];
	cornerTwoX = points[2];
	cornerTwoY = points[3];
	cornerThreeX = points[4];
	cornerThreeY = points[5];

	context.beginPath();
	context.moveTo(cornerOneX,cornerOneY);
	context.lineTo(cornerTwoX, cornerTwoY);
	context.lineTo(cornerThreeX, cornerThreeY);
	context.closePath();
	context.strokeStyle = 'black';
	context.stroke();

	console.log("finished drawing triangle");
}

function drawRotatedRectangle(){
	cornerOneX = points[0];
	cornerOneY = points[1];
	cornerTwoX = points[2];
	cornerTwoY = points[3];
	cornerThreeX = points[4];
	cornerThreeY = points[5];
	cornerFourX = points[6];
	cornerFourY = points[7];

	context.beginPath();
	context.moveTo(cornerOneX, cornerOneY);
	context.lineTo(cornerTwoX, cornerTwoY);
	context.lineTo(cornerThreeX, cornerThreeY);
	context.lineTo(cornerFourX, cornerFourY);
	context.lineTo(cornerOneX, cornerOneY);
	context.closePath();
	context.strokeStyle = 'black';
	context.stroke();

	console.log("finished drawing rectangle");



}




function drawOldPic(){
	for(var v = 0; v < prevArrayOfPixels.length-2; v+=2)
	{
		var x = prevArrayOfPixels[v];
		var y = prevArrayOfPixels[v+1];		
		context.fillRect(x, y, 5, 5);
	}
}



function getPos(evt) {
	//var context = c.getContext("2d");
	var rect = c.getBoundingClientRect();
	var x = parseInt(evt.clientX - rect.left);
	var y = parseInt(evt.clientY - rect.top);
	//var imgData = context.getImageData(evt.clientY,evt.clientX, 1, 1);		//get color of pixel
	var imgData = context.getImageData(20, 20, 150, 100);
	//var r = imgData.data[0]
	//var g = imgData.data[1];
	//var b = imgData.data[2];
	
	//arrayOfPixels.push([x, y, r, g, b]);
	arrayOfPixels.push([x,y]);

};

c.addEventListener('mousedown', function(evt){
	clicked = true;
	getPos(evt);
	prevArrayOfPixels = [];
}, false);

c.addEventListener('mousemove', function(evt) {
	if(clicked == false) { 
		return;
	}	
	getPos(evt);
}, false);

/*c.addEventListener('mouseup', function(evt) {
	clicked    = false;
	var width  = document.getElementById("canvas").width;
	var height = document.getElementById("canvas").height;
	var size   = [width, height];
	console.log(size);
	$("#array").attr("readonly", "false");
	$("#array").val(arrayOfPixels);
	$("#size").attr("readonly", "false");
	$("#size").val(size);
	arrayOfPixels = [];

	var input_string =  $$("input#textfield").val();

	$.ajax({
	        type: 'POST',
	        url: "test.py",
	        data: {param:  }, //passing some input here
	        dataType: "text",
	        success: function(response){
	           output = response;
	           alert(output);
	   }
	}).done(function(data){
	    console.log(data);
	    alert(data);
	});

	//document.getElementById("form").submit();
	
},false);
*/

//jquery!!


$("#canvas").mouseup(function(){
	clicked    = false;
	var width  = $("#canvas").width();
	var height = $("#canvas").height();
	var size   = [width, height];
	$("#array").attr("readonly", "false");
	$("#array").val(arrayOfPixels);
	$("#size").attr("readonly", "false");
	$("#size").val(size);
	arrayOfPixels = [];


	// console.log("ajaxtime");
	// $.ajax({
	//         type: 'GET',
	//         url: "test.py",
	//         data: "data!", //passing some input here
	//         success: function(data){




	//            output = data;
	//            console.log(output);
	//    }
	// }).done(function(data){
	//     console.log(data);
	//     alert(data);
	// });

	// $.ajax({
	//         type: 'POST',
	//         url: "test.py",
	//         data: "test", //passing some input here
	//         dataType: "text",
	//         success: function(json){
	//            output = json.foo;
	//            console.log(json.foo);
	//            console.log(json);
	//            //alert(output);
	//    }
	// });







	document.getElementById("form").submit();
	
});
// function defLine(gepx1,gepy1,gepx2,gepy2)
// {
// 	var templine = {tag:"line", epx1:gepx1, epy1:gepy1, epx2:gepx2, epy2:gepy2};
// //	templine.epx1 = epx1;
// //	templine.epx2 = epx2;
// //	templine.epy1 = epy1;
// //	templine.epy2 = epy2;
// 	return templine;
// }

// function defEllipse(gcx,gcy,grx,gry,gra)
// {
// //	this.cx = cy;
// //	this.cy = cy;
// //	this.rx = rx;
// //	this.ry = ry;
// //	this.ra = ra;
// 	var tempEllipse = {tag:"ellipse", cx:gcx , cy:gcy , rx:grx , ry:gry , ra:gra};
// 	return tempEllipse;
// }
// function redraw()
// {
// 	for(var i = 0; i < shapeHolder.length; i++)
// 	{
// 		if(shapeHolder[i] == "line")
// 		{
// 			context.beginPath();
// 			context.moveTo(shapeHolder[i].epx1,shapeHolder[i].epy1);
// 			context.lineTo(shapeHolder[i].epx2, shapeHolder[i].epy2);
// 			context.stroke();
// 		}
// 		else if(shapeHolder[i] == "ellipse")
// 		{
// 			context.beginPath();
// 			context.ellipse(shapeHolder[i].cx,shapeHolder[i].cy,shapeHolder[i].rx,shapeHolder[i].ry,shapeHolder[i].ra,0, 2*Math.PI);
// 			context.stroke();
// 		}
// 	}
// }


//hover tool bar
// $("toolbar").hide();
// $('holder').css("display", "inline-block").hover(function(e){
//     e.preventDefault();
//     $('#toolbar').css( 'position', 'absolute' );
//     $('#toolbar').show();
// },function(){
//   $('#questionMarkId').hide();

// }).on("mousemove", function(e) { 
//     $('#toolbar').css( 'top', e.pageY + 10 );
//     $('#toolbar').css( 'left', e.pageX + 10 );
// });






</script>








