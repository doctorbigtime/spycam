<html>
<head>
<script>
var docElem = document.documentElement;
var barWidth = Math.max(docElem.clientWidth/20.0, 20);
var barHeight = Math.max(docElem.clientHeight - 50, 50);
var barX = 10
var barY = 10


function GET(url, callback) 
{
    var req = new XMLHttpRequest();
    req.onreadystatechange = function() {
        if(req.readyState == 4 && req.status == 200)
            callback(req.responseText);
    }
    req.open("GET", url, true);
    req.send(null);
}

var dates = []

//GET("http://fortas.org/dates.json", function (text) {
GET("/{{curr_dir}}/dates.json", function (text) {
    var json = JSON.parse(text);

    for(i = 0; i < json.dates.length; ++i)
        dates[i] = new Date(json.dates[i])
});

// random dates.

function pctToDate(pct) {
    var index = parseInt(pct * dates.length);
    return dates[index];
}

function zeroPad(n, len)
{
    if((''+n).length > len) return ''+n;
    var zeros = '';
    for(i = 0; i < len; ++i) zeros += '0';
    return (zeros + n).slice(-len);
}

function dateToFilename(date)
{
    var filename = zeroPad(date.getFullYear(),4) + zeroPad(date.getMonth()+1,2)
                   + zeroPad(date.getDate(),2) + zeroPad(date.getHours(),2)
                   + zeroPad(date.getMinutes(),2) + zeroPad(date.getSeconds(),2)
                   // TODO:
                   + '-00.jpg';
    return filename;
}

</script>
<h1>
Path: {{curr_dir}}<br>
</h1>
<div style="width=: 100%">
    <canvas id="myCanvas"
        style="border:1px solid #d3d3d3;"
        onMouseMove="print_coord(event)" 
        onMouseOut="clear_coord()"
        onClick="show_image(event)"
        >
    Your browser does not support the canvas element.
    </canvas>
    <div id="xycoord" 
        style="position: absolute; background-color: coral; color: white;">
    </div>
    <div id="thumb" 
        style="position: absolute; background-color: black; color: white;">
        <img id="thumbnail" src="">
    </div>

    <div id="image"
        style="float: right; height: 500px; width: 700px; background-color: black; color: white;">
        <img id="big_image" src="">
    </div>
</div>

<script>
var canvas = document.getElementById("myCanvas");
canvas.width = barWidth + 20;
canvas.height = barHeight + 20;

function show_image(e)
{
    x = e.clientX;
    y = e.clientY - 10;
    pct = (y - barY)/barHeight;

    image = document.getElementById("big_image");
    when = pctToDate(pct);
    image.src = '/picture/{{curr_dir}}/' + dateToFilename(when);
}

function print_coord(e)
{
    x = e.clientX;
    y = e.clientY - 10;
    if(y < barY || y > barHeight + barY)
        return clear_coord();
    pct = (y - barY)/barHeight;
    xycoord = document.getElementById("xycoord");
    xycoord.style.top = y;
    xycoord.style.left = (barWidth + 25) + "px";

    var date = pctToDate(pct);
    text = "Coord: (" + x + ", " + y + " [" + (pct*100.0).toFixed(2) + "%] :: " + date;
    xycoord.innerHTML = text;

    thumb = document.getElementById("thumb");
    thumb.style.top = y + 20;
    thumb.style.left = (barWidth + 30);
    nail = document.getElementById("thumbnail");
    nail.src = '/thumb/{{curr_dir}}/' + dateToFilename(date);
}
function clear_coord()
{
    document.getElementById("xycoord").innerHTML = "";
}
var ctx = canvas.getContext("2d");

var grd = ctx.createLinearGradient(0,0,0,barHeight);
grd.addColorStop(0, "#FFCC00")
grd.addColorStop(1, "#FFCCFF")

ctx.fillStyle = grd;
ctx.fillRect(barX,barY,barWidth,barHeight);

// write heigh/width
e = document.documentElement;
ctx.save();
ctx.rotate(Math.PI/2);
ctx.font = "18px Arial";
//ctx.textAlign = "center";
ctx.fillStyle = "black";
ctx.fillText("width: " + e.clientWidth + " height: " + e.clientHeight
            , 100, -20);
ctx.restore();
</script>
</head>
</html>
