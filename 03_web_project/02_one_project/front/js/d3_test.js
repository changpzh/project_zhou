/**
 * Created by zhou on 16-9-1.
 */

var svg = d3.select('svg');

var data = [{"tag":"abc","val":123}]
    data2 = [{"tag":"ijk","val":321}]

var dataChoose = data;

var myBarGraph = svg.selectAll('rect')
    .data(dataChoose)
    .enter()
    .append('rect')
    .attr({
      x: 160,
      y: 135,
      height: 20,
      width: function(d) { return d.val; },
      fill: 'black'
    });

var updateBarGraph = function() {
    myBarGraph
    .data(dataChoose)
    .transition()
    .duration(1000)
    .attr('width', function(d) { return d.val; })
}

var myText = svg.append('text')
    .data(dataChoose)
    .attr('x', 129)
    .attr('y', 150)
    .attr('fill', '#000')
    .classed('dataChoose', true)
    .text(function(d) { return d.tag })

svg.on("click", function() {
        if (dataChoose == data) {
            dataChoose = data2;
        } else {
        dataChoose = data;
        }
        redrawText();
        updateBarGraph();
    });

function redrawText() {
    myText
    .data(dataChoose)
    .transition()
    .duration(1000)
    .style("opacity", 0)
    .transition().duration(500)
    .style("opacity", 1)
    .text(function(d) { return d.tag })
}