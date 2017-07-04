/**
 * Created by changpzh on 2016/8/23.
 */

var data = [  {'name':"fzm", data:[{ "day": 2016/08/08, "result" : "fail" },
                                                {"day": 2016/08/09,"result" : "pass"},
                                                {"day": 2016/08/10,"result" : "pass"},
                                                {"day": 2016/08/11,"result" : "-"},
                                                {"day": 2016/08/12,"result" : "pass"},
                                                {"day": 2016/08/13,"result" : "-"},
                                                {"day": 2016/08/14,"result" : "pass"}]},
    {'name':"trunk", data:[{ "day": 2016/08/08, "result" : "fail" },
                                                {"day": 2016/08/09,"result" : "pass"},
                                                {"day": 2016/08/10,"result" : "pass"},
                                                {"day": 2016/08/11,"result" : "-"},
                                                {"day": 2016/08/12,"result" : "pass"},
                                                {"day": 2016/08/13,"result" : "-"},
                                                {"day": 2016/08/14,"result" : "pass"}]},
    {'name':"tdd-macro", data:[{ "day": 2016/08/08, "result" : "fail" },
                                                {"day": 2016/08/09,"result" : "pass"},
                                                {"day": 2016/08/10,"result" : "pass"},
                                                {"day": 2016/08/11,"result" : "-"},
                                                {"day": 2016/08/12,"result" : "pass"},
                                                {"day": 2016/08/13,"result" : "-"},
                                                {"day": 2016/08/14,"result" : "pass"}]}];


var DAYS_NUM = 30;
var svg =d3.select("#graph").append("svg").attr("width",600).attr("height",500);
var ii = 0;
var myWidth = 110;
var myHeight = 30;
var radus = 15;

var graph_width = $("#graph").width();
var margin = {top: 30, right: 20, bottom: 30, left: 20};

console.log("graph----width"+graph_width);


var pass_color = "#4caf50";//#2DA33C";
var fail_color = " #f44336";// "#EA9999";
var noexe_color = "#E7EAEA";//"#BEBEBE";

function labcolor(d) {
  return d._children ? "#3182bd" : d.children ? "#c6dbef" : "#fd8d3c";
}

data.forEach(function (n, i) {
    n.x = (i+1) * myHeight*2;
});

var nodes = svg.selectAll("nodeg").data(data, function (dd) {return dd.id || (dd.id = ++ii); });
var nodesEnter = nodes.enter().append("g")
    .attr('class', "nodeg")
    .attr('transform', function(d) { return "translate(0," + d.x + ")"; });
var labEnter = nodesEnter.append("g")
    .attr("class", "info")
    .attr("transform", function(d){ return "translate(0," + "0" + ")"; });
labEnter.append("rect")
    .attr("y", -myHeight/2)
    .attr("height", myHeight)
    .attr("width", myWidth)
    .style("fill", labcolor)

labEnter.append("line")
    .attr("x1", function(d) { return 110; })
    .attr("y1", function(d) { return 0;})
    .attr("x2",function(d){return graph_width;})
    .attr('y2',0)
    .style("stroke-dasharray", "5, 5")
    .attr("stroke", "gray")
    //.attr("width", "1")
labEnter.append("text")
    .attr("dy", 3.5)
    .attr("dx", 5.5)
    .text(function(d) { return ((d.name||'').toUpperCase()) });

var cir = nodes.selectAll("day").data(function(d) {return d.data;});
var cirEnter = cir.enter().append("g")
    .attr("class", "day")
    .attr("transform", function(d, j) { return "translate(" + (myWidth + (j+1)*radus*4) + ",0)"; });

cirEnter.append("circle")
    .attr("r", radus)
    .style("fill", function (d){return d.result == "pass"?pass_color:(d.result == "fail"?fail_color:noexe_color);})



//append first line
function scenary2(){
    var data2 = [
  {
   "x_axis": 30,
   "y_axis": 30,
   "radius": 20,
   "color" : "green"
  }, {
   "x_axis": 70,
   "y_axis": 70,
   "radius": 20,
   "color" : "purple"
  }, {
   "x_axis": 110,
   "y_axis": 100,
   "radius": 20,
   "color" : "red"
}];

    var myWidth = $("body").width();
    var xdomain = [];
    for(var i=0;i<data2.length;i++){
        xdomain.push(i);
    }
    var y = d3.scale.ordinal()
        .rangeRoundBands([40, myWidth - 40])
        .domain(xdomain);

    var bodySelection = d3.select("body");
    var svgSelection = bodySelection.append("svg").attr("width",500).attr("height",500);

    var svgEnter = svgSelection.append("g").attr("class","days").attr("transform", "translate(50,0)");
    var cir = svgEnter.selectAll("day").data(data2).enter().append("g").attr("class","day").attr("transform", function(d, i) {return "translate(0," + y(i) + ")"})

    cir.append("circle").attr("r", function(d) {return 15;}).style("fill", function(d) {return d.color;})

}

function getMax_xy(jsonArr){
    var jsonArr = [
      { "x_axis": 10, "y_axis": 10, "height": 20, "width":20, "color" : "green" },
      { "x_axis": 160, "y_axis": 40, "height": 20, "width":20, "color" : "purple" },
      { "x_axis": 70, "y_axis": 70, "height": 20, "width":20, "color" : "red" }];

    var max_x = 0; //This will be updated to be the max x-coordinate
    var max_y = 0; //This will be updated to be the max y-coordinate

    //We loop through our jsonRectangles array
    for (var i = 0; i < jsonArr.length; i++) {

      var temp_x, temp_y;

      // To get the farthest right hand point, we need to add the x-coordinate and the width
      var temp_x = jsonArr[i].x_axis + jsonArr[i].width;

      // To get the farthest bottom point, we need to add the y-coordinate and the height
      var temp_y = jsonArr[i].y_axis + jsonArr[i].height;

      /**
      * If the temporary x-coordinate is bigger than the max_x,
      * make the max_x equal to the temp_x
      * otherwise, do nothing.
      */
      if ( temp_x >= max_x ) {
        max_x = temp_x;
      }

      /**
      * If the temporary y-coordinate is bigger than the max_y,
      * make the max_y equal to the temp_y
      * otherwise, do nothing.
      */
      if ( temp_y >= max_y ) {
        max_y = temp_y;
      }

    }//End of the loop

    return (max_x, max_y)
}


