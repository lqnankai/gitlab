var neurons = [];
var synapses = [];
var ipsGroupnum = 0;
var msmGroupnum = 0;
var width = 1300;
var height = 1300; 
var color = []
var svg;
var defs;
var arrowMarker;
var ipsmap = {};
var msmGroupmap = {}
function svginit() {
	
	generateColor();
	svg = d3.select(".algorithmfield")
	.append("svg")
	.attr("width", width)
	.attr("height", height);
	
	defs = svg.append("defs");
	arrowMarker = defs.append("marker")
	.attr("id","arrow")
	.attr("markerUnits","strokeWidth")
    .attr("markerWidth","12")
    .attr("markerHeight","12")
    .attr("viewBox","0 0 12 12") 
    .attr("refX","6")
    .attr("refY","6")
    .attr("orient","auto");

//	var arrow_path = "M2,2 L2,10 L2,2";
//		
//	arrowMarker.append("path")
//	.attr("d",arrow_path)
//	.attr("fill","#CCCCCC");
}

function generateColor() {
	for(var i = 0; i < 60; i++) {
		var colorStr=Math.floor(Math.random()*0xFFFFFF).toString(16).toUpperCase();
		c =  "#"+"000000".substring(0,6-colorStr)+colorStr;
		color.push(c);
	}
}
function draw() {
	//alert("haha");
	var updateNeurons = svg.selectAll("circle")
					.data(neurons);
	var enterNeurons = updateNeurons.enter();
	var exitNeurons = updateNeurons.exit();
	
	//update function processing
	updateNeurons.attr("r",function(d) {
		if(d.area == "IPS") return 15;
		else if(d.area == "MSM") return 8;
	})
	.attr("cx",function(d,i){
		if(d.area == "IPS") return d.GroupID * (width/(ipsGroupnum+1));
		//else if(d.area == "MSM") return d.GroupID * (width/(msmGroupnum+1));
		//if(d.area == "IPS") return d.Index * 25;
		else if(d.area == "MSM") return d.Index * 25 + 30;
	})
	.attr("cy",function(d,i){
		if(d.area == "IPS") return d.Index * 25;
		//else if(d.area == "MSM") return d.Index * 25 + 30;
		//if(d.area == "IPS") return d.GroupID * (height/(ipsGroupnum+1));
		else if(d.area == "MSM") return d.GroupID * 50 + 40;//return d.GroupID * (height/(msmGroupnum+1));
	})
	.style("fill",function(d){
		if(d.area == "IPS") return "#FFFFFF";
		else if(d.area == "MSM") return color[d.Index-1];
	})
	.on("mouseover",function(d){
		d3.select(this).style("color","red");
	});
	
	//enter function processing
	enterNeurons.append("circle")
	.attr("r",function(d) {
		if(d.area == "IPS") return 15;
		else if(d.area == "MSM") return 8;
	})
	.attr("cx",function(d,i){
		if(d.area == "IPS") return d.GroupID * (width/(ipsGroupnum+1));
		//else if(d.area == "MSM") return d.GroupID * (width/(msmGroupnum+1));
		//if(d.area == "IPS") return d.Index * 25;
		else if(d.area == "MSM") return d.Index * 25 + 30;
	})
	.attr("cy",function(d,i){
		if(d.area == "IPS") return d.Index * 25;
		//else if(d.area == "MSM") return d.Index * 25 + 30;
		//if(d.area == "IPS") return d.GroupID * (height/(ipsGroupnum+1));
		else if(d.area == "MSM") return d.GroupID * 50 + 40;//return d.GroupID * (height/(msmGroupnum+1));
	})
	.style("fill",function(d){
		if(d.area == "IPS") return "#FFFFFF";
		else if(d.area == "MSM") return color[d.Index-1];
	})
	.on("mouseover",function(d){
		d3.select(this).style("fill","red");
	});
	
	//exit function processing
	exitNeurons.remove();
}
function syn_draw() {
	
	
	var curve_path = "M20,70 L160,80 L200,90";
	var updatecurve = svg.selectAll("line")
					.data(synapses);
	
	var entercurve = updatecurve.enter();
	var exitcurve = updatecurve.exit();
	// update function processing
	
	updatecurve.attr("x1",function(d) {
		if(d.type == 2) {
			return d.SgroupID * (width/(ipsGroupnum+1));
		}
//		else if(d.type == 1 || d.type == 0) {
//			return d.SgroupID * (width/(msmGroupnum+1));
//		}
//		if(d.type == 2) {
//			return d.Sindex * 25;
//		}
		if(d.type == 1 || d.type == 0) {
			return d.Sindex * 25 + 30;
		}
	})
	.attr("y1",function(d) {
		if(d.type == 2) return d.Sindex * 25;
		//else if(d.type ==1 || d.type == 0) return d.Sindex * 25 + 30;
		//if(d.type == 2) return d.SgroupID * (height/(ipsGroupnum+1));
		if(d.type ==1 || d.type == 0) return d.SgroupID * 50 + 40;
		
	})
	.attr("x2",function(d) {
		//return d.TgroupID * (width/(msmGroupnum+1));
		return d.Tindex * 25 +30;
		
	})
	.attr("y2",function(d) {
		//return d.Tindex * 25 +30;
		return d.TgroupID * 50 + 40;
	})
	.attr("stroke",function(d) {
		if(d.type ==0) return "#FFFF00";
		else if(d.weight > 0) return "#FF6666";
		else return "#CCCCCC";
	})
	.attr("stroke-width",function(d) {
		if(d.weight > 0) return 1;
		else return 0.5;
	})
	.attr("marker-end","url(#arrow)");
	
	//enter function processing
	entercurve.append("line")
	.attr("x1",function(d) {
		if(d.type == 2) {
			return d.SgroupID * (width/(ipsGroupnum+1));
		}
//		if(d.type == 1 || d.type == 0) {
//			return d.SgroupID * (width/(msmGroupnum+1));
//		}
//		if(d.type == 2) {
//			return d.Sindex * 25;
//		}
		if(d.type == 1 || d.type == 0) {
			return d.Sindex * 25 + 30;
		}
		
	})
	.attr("y1",function(d) {
		if(d.type == 2) return d.Sindex * 25;
		//if(d.type ==1 || d.type == 0) return d.Sindex * 25 + 30;
		//if(d.type == 2) return d.SgroupID * (height/(ipsGroupnum+1));
		if(d.type ==1 || d.type == 0) return d.SgroupID * 50 + 40;
		
	})
	.attr("x2",function(d) {
		//return d.TgroupID * (width/(msmGroupnum+1));
		return d.Tindex * 25 +30;
	})
	.attr("y2",function(d) {
		//return d.Tindex * 25 +30;
		return d.TgroupID * 50 + 40;
	})
	.attr("stroke",function(d){
		//if(d.type != 0 && d.weight > 0) return "#FF6666";
		if(d.type ==0) return "#FFFF00";
		else if(d.weight > 0) return "#FF6666";
		else return "#CCCCCC";
	})
	.attr("stroke-width",function(d) {
		if(d.weight > 0) return 1;
		else return 0.5;
	})
	.attr("marker-end","url(#arrow)");
	
	//exit function processing
	exitcurve.remove();
	
}
function ips_show(jsondata) {
	
	
	var data = JSON.parse(jsondata);
	if(ipsmap.hasOwnProperty(data.Name) == false) {
		neurons = neurons.concat(data.Neuron);
		ipsGroupnum = data.GroupID;
		ipsmap[data.Name] = 1;
		draw();
	}
	syn_draw();
}

function msm_show(jsondata) {
	
	var data = JSON.parse(jsondata);
	var dic = data.Neuron;
	if(msmGroupmap.hasOwnProperty(data.GroupNum.toString()) == false) {
		neurons = neurons.concat(dic.Neuron);
		if(data.GroupNum > msmGroupnum) msmGroupnum = data.GroupNum;
		draw();
	}
	for(i = 0; i < dic.Neuron.length; i++){
		var synlist = dic.Neuron[i].synapses;
		synapses = synapses.concat(synlist);
	}
	syn_draw();
}