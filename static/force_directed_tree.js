
var w = document.documentElement.clientWidth,
    h = document.documentElement.clientHeight,
    r = 10,
    fill = d3.scale.category20();

function loadGraph(json) {
  var force = d3.layout.force()
    .charge(-200)
    .linkDistance(100)
    .size([w, h]);
  jQuery('svg').remove();
  var svg = d3.select("body").append("svg:svg")
      .attr("width", w)
      .attr("height", h);
    var link = svg.selectAll("line")
        .data(json.links)
      .enter().append("svg:line");

  // Create the groups under svg
  var gnodes = svg.selectAll('g.gnode')
    .data(json.nodes)
    .enter()
    .append('g')
    .classed('gnode', true);

  // Add one circle in each group
  var node = gnodes.append("circle")
    .attr("class", "node")
    .attr("r", r)
    .style("fill", function(d) { return fill(d.group); })
    .call(force.drag)
    .on("mouseover", function(){d3.select(this).style("fill", "blue");})
    .on("mouseout", function(){d3.select(this).style("fill", function(d) { return fill(d.group); });})
    .on("mousedown", function() {remuser(this.__data__.name)});

  // Append the labels to each group
  var labels = gnodes.append("text")
    .text(function(d) { return d.name; });

  force.on("tick", function() {
    // Update the links
    link.attr("x1", function(d) { return d.source.x; })
      .attr("y1", function(d) { return d.source.y; })
      .attr("x2", function(d) { return d.target.x; })
      .attr("y2", function(d) { return d.target.y; });

    // Translate the groups
    gnodes.attr("transform", function(d) { 
      return 'translate(' + [d.x, d.y] + ')'; 
    });    

  });

  force
      .nodes(json.nodes)
      .links(json.links)
      .on("tick", tick)
      .start();

  function tick(e) {

    // Push sources up and targets down to form a weak tree.
    var k = 10 * e.alpha;
    json.links.forEach(function(d, i) {
      d.source.y -= k;
      d.target.y += k;
    });

    node.attr("cx", function(d) { return d.x; })
        .attr("cy", function(d) { return d.y+100; });

    labels.attr("x", function(d) { return (d.x-15); })
          .attr("y", function(d) { return d.y+120; })
          .attr("font-size", ".75em");

    link.attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y+100; })
        .attr("x2", function(d) { return (d.target.x); })
        .attr("y2", function(d) { return d.target.y+100; });
  }
};

window.data = {
  "nodes": [
    {"name": "datacenter"},
    {"name": "rack0"},
    {"name": "rack1"},
    {"name": "rack2"}
  ],
  "links": [
    {"source": 0, "target": 1},
    {"source": 0, "target": 2},
    {"source": 0, "target": 3}
  ]
}