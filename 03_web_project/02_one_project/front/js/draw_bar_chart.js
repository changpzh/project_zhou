/**
 * Created by zhou on 16-9-1.
 */

var dataPass = [4, 8, 15, 16, 23, 42];
var dataFail = [4, 8, 15, 16, 23, 42];

var data = [4, 8, 15, 16, 23, 42];

var totalCaseNum = 60;
var width = 500,
    barHeight = 20;

var x = d3.scale.linear()
    .domain([0, totalCaseNum])
    .range([0, width]);

var chart = d3.select(".chart")
    .attr("width", width)
    .attr("height", barHeight * data.length);

var bar = chart.selectAll("g")
    .data(data)
    .enter().append("g")
    .attr("transform", function(d, i) { return "translate(0," + i * barHeight + ")"; });

bar.append("rect")
    .attr("width", x)
    .attr("height", barHeight - 1);

bar.append("text")
    .attr("x", function(d) { return x(d) - 5; })
    .attr("y", barHeight / 2)
    .attr("dy", ".35em")
    .text(function(d) { return d; });