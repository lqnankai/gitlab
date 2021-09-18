// define the circle data set
var nodes = [{groupID:1,index:1},{groupID:1,index:2},{groupID:1,index:3},
             {groupID:2,index:1},{groupID:2,index:2},{groupID:2,index:3}];

var edges = [{sgroupID:1,sindex:1,tgroupID:2,tindex:1},{sgroupID:1,sindex:2,tgroupID:2,tindex:2},
             {sgroupID:1,sindex:3,tgroupID:2,tindex:3},{sgroupID:1,sindex:1,tgroupID:2,tindex:3}];

// size of the canvas
var width = 1000
var height = 1000

// add a svg in the body
var svg = d3.select("body")
	.append("svg")
	.attr("width", width)
	.attr("height", height);

var neurons = svg.selectAll("circle")
	.data(nodes)
	.enter()
	.append("circle")
	.attr("r",10)
	.attr("cx",function(d,i){
		return d.index * 40;
	})
	.attr("cy",function(d,i){
		return d.groupID * 40
	})
	.style("fill",function(d,i){
		if(d.groupID == 1) return "green";
		else return "yellow";
	});

var synapses = svg.selectAll("line")
	.data(edges)
	.enter()
	.append("line")
	.attr("stroke","#ccc")
	.attr("stroke-width",1)
	.attr("x1",function(d,i) {
		return d.sindex * 40
	})
	.attr("y1",function(d) {
		return d.sgroupID * 40
	})
	.attr("x2",function(d,i) {
		return d.tindex * 40
	})
	.attr("y2",function(d,i) {
		return d.tgroupID * 40
	});
	
neurons.transition()
	.duration(1500)
	.attr("cx",function(d,i){
		return d.groupID * 40
	})
	.attr("cy",function(d,i){
		return d.index * 40
	})

synapses.transition()
	.duration(1500)
	.attr("x1",function(d,i){
		return d.sgroupID * 40
	})
	.attr("y1",function(d){
		return d.sindex * 40
	})
	.attr("x2",function(d){
		return d.tgroupID * 40
	})
	.attr("y2",function(d){
		return d.tindex * 40
	})
	