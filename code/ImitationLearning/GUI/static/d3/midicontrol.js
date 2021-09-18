var currentState = "None";
var g_data = '';
var w = 1800;
var h = 1000; 
var vis;
var color = [];
var episode = [];
var url = "ws://localhost:61614/stomp";
var login = 'admin';
var passcode = 'admin';
var destination = "/Queue/SampleQueue";
var force = d3.layout.force();
var link,node,nodeEnter;
var nodes = force.nodes();
var links = force.links();
var flag = 1;
client = Stomp.client(url);

/*****************  function   *********************/
function generateColor() {
	for(var i = 0; i < 3; i++) {
		var colorStr=Math.floor(Math.random()*0xFFFFFF).toString(16).toUpperCase();
		c =  "#"+"000000".substring(0,6-colorStr)+colorStr;
		color.push(c);
	}
}

function midi_init() {
	generateColor();
	vis = d3.select("#graphfield")
    .append("svg:svg")
    .attr("width", w)
    .attr("height", h)
    .attr("id", "svg")
    .attr("pointer-events", "all")
    .attr("viewBox", "0 0 " + w + " " + h)
    .attr("perserveAspectRatio", "xMinYMid")
    .append('svg:g');
	'use strict';

    var
        divLog = document.getElementById('log'),
        divInputs = document.getElementById('inputs'),
        divOutputs = document.getElementById('outputs'),
        midiAccess,
        checkboxMIDIInOnChange,
        checkboxMIDIOutOnChange,
        activeInputs = {},
        activeOutputs = {};


    if (navigator.requestMIDIAccess !== undefined) {
        navigator.requestMIDIAccess().then(

            function onFulfilled(access) {
                midiAccess = access;
                console.log(midiAccess);

                // create list of all currently connected MIDI devices
                showMIDIPorts();

                // update the device list when devices get connected, disconnected, opened or closed
                midiAccess.addEventListener('statechange', function (e) {
                    var port = e.port;
                    var div = port.type === 'input' ? divInputs : divOutputs;
                    var listener = port.type === 'input' ? checkboxMIDIInOnChange : checkboxMIDIOutOnChange;
                    var activePorts = port.type === 'input' ? activeInputs : activeOutputs;
                    var checkbox = document.getElementById(port.type + port.id);
                    var label;

                    // device disconnected
                    if (port.state === 'disconnected' && checkbox !== null) {
                        div.removeChild(checkbox.parentNode.nextSibling); // remove the <br> after the checkbox
                        div.removeChild(checkbox.parentNode); // remove the label and the checkbox
                        port.close();
                        delete activePorts[port.type + port.id];

                        // new device connected
                    } else if (port.state === 'connected' && checkbox === null) {
                        label = document.createElement('label');
                        checkbox = document.createElement('input');
                        checkbox.type = 'checkbox';
                        checkbox.id = port.type + port.id;
                        checkbox.addEventListener('change', listener, false);
                        label.appendChild(checkbox);
                        label.appendChild(document.createTextNode(port.name + ' (' + port.state + ', ' + port.connection + ')'));
                        div.appendChild(label);
                        div.appendChild(document.createElement('br'));
                    }
                }, false);
            },

            function onRejected(e) {
                divInputs.innerHTML = e.message;
                divOutputs.innerHTML = '';
            }
        );
    }

    // browsers without WebMIDI API and WebMIDIAPIShim not present
    else {
    	console.log('No access to MIDI devices: browser does not support WebMIDI API, please use the WebMIDIAPIShim together with the Jazz plugin');
        divInputs.innerHTML = 'No access to MIDI devices: browser does not support WebMIDI API, please use the WebMIDIAPIShim together with the Jazz plugin';
        divOutputs.innerHTML = '';
    }


    function showMIDIPorts() {
        var
            html,
            checkbox,
            checkboxes,
            inputs, outputs,
            i, maxi;

        inputs = midiAccess.inputs;
        html = '<h4 style = "color:white">midi inputs:</h4>';
        inputs.forEach(function (port) {
            html += '<label style = "color:white"><input type="checkbox" id="' + port.type + port.id + '">' + port.name + ' (' + port.state + ', ' + port.connection + ')</label><br>';
        });
        divInputs.innerHTML = html;

        outputs = midiAccess.outputs;
        html = '<h4 style = "color:white">midi outputs:</h4>';
        outputs.forEach(function (port) {
            html += '<label style = "color:white"><input type="checkbox"  id="' + port.type + port.id + '">' + port.name + ' (' + port.state + ', ' + port.connection + ')</label><br>';
        });
        divOutputs.innerHTML = html;

        checkboxes = document.querySelectorAll('#inputs input[type="checkbox"]');
        for (i = 0, maxi = checkboxes.length; i < maxi; i++) {
            checkbox = checkboxes[i];
            checkbox.addEventListener('change', checkboxMIDIInOnChange, false);
        }

        checkboxes = document.querySelectorAll('#outputs input[type="checkbox"]');
        for (i = 0, maxi = checkboxes.length; i < maxi; i++) {
            checkbox = checkboxes[i];
            checkbox.addEventListener('change', checkboxMIDIOutOnChange, false);
        }
    }


    // handle incoming MIDI messages
    function inputListener(midimessageEvent) {
        var port, portId,
            data = midimessageEvent.data,
            type = data[0],
            data1 = data[1],
            velocity = data[2];
        	id = "#"+ data1;
            switch (type) {
            	case 144: // noteOn
            		if (velocity > 0) {
            			$(id).css("background-color","FFA500");
            			episode.push(data1);
            			
            		} else {
            			var cname = $(id).attr("class");
            			if(cname.indexOf("white") != -1 )
            				$(id).css("background-color","ffffff");
            			else
            				$(id).css("background-color","000000");
            		}
            		break;
            	case 128: // noteOff
            		var cname = $(id).attr("class");
        			if(cname.indexOf("white") != -1)
        				$(id).css("background-color","ffffff");
        			else
        				$(id).css("background-color","000000");
            		break;
            }
    


        // do something graphical with the incoming midi data
        divLog.innerHTML = type + ' ' + data1 + ' ' + velocity + '<br>' + divLog.innerHTML;

        for (portId in activeOutputs) {
            if (activeOutputs.hasOwnProperty(portId)) {
                port = activeOutputs[portId];
                port.send(data);
            }
        }
    }


    checkboxMIDIInOnChange = function () {
        // port id is the same a the checkbox id
        var id = this.id;
        var port = midiAccess.inputs.get(id.replace('input', ''));
        var cb = this;
        if (this.checked === true) {
            activeInputs[id] = port;
            port.addEventListener('midimessage', inputListener, false);
            port.addEventListener('statechange', function () {
                cb.nextSibling.nodeValue = port.name + ' (' + port.state + ', ' + port.connection + ')';
            }, false);
            // we have to open the port explicitly because we don't use port.onmidimessage this time
            port.open();
        } else {
            delete activeInputs[id];
            // port.close() will also remove all eventlisteners
            port.close();
        }
    };


    checkboxMIDIOutOnChange = function () {
        // port id is the same a the checkbox id
        var id = this.id;
        var port = midiAccess.outputs.get(id.replace('output', ''));
        var cb = this;
        if (this.checked === true) {
            activeOutputs[id] = port;
            port.addEventListener('statechange', function () {
                cb.nextSibling.nodeValue = port.name + ' (' + port.state + ', ' + port.connection + ')';
            }, false);
            port.open();
        } else {
            delete activeOutputs[id];
            port.close();
        }
    };
}
var onconnect = function(frame) {
	client.subscribe(destination,function(message){
		console.log(message.body);
		test(message.body);
		//setTimeout(after,10000);
	});
};

client.connect(login,passcode,onconnect);

function OpenFiles() {
	$("#files").click();
}

function FileImport() {
	var f = document.getElementById("files").files[0];
	var currentMIDIFile = f.name;
	strs = currentMIDIFile.split(".");
	$("#musicname").text(strs[0]);
	currentState = "Remember";
	$.get("http://localhost:8888/midicontrol",{State:currentState,MusicName:currentMIDIFile},function(data,status){
		g_data = data;
		//ips_show(data);
	})	
}

function task1() {
	$("#AllNeurons").css("background-color","ffff66");
	$("#NoteNeurons").css("background-color","e6e6e6");
	$("#TimeNeurons").css("background-color","e6e6e6");
	//console.log(g_data);
	//ips_show(g_data);
	test_show();
	
	
}

function task2() {
	//alert("2");
	$("#AllNeurons").css("background-color","e6e6e6");
	$("#NoteNeurons").css("background-color","ffff66");
	$("#TimeNeurons").css("background-color","e6e6e6");
	
}

function task3() {
	//alert("3");
	$("#AllNeurons").css("background-color","e6e6e6");
	$("#NoteNeurons").css("background-color","e6e6e6");
	$("#TimeNeurons").css("background-color","ffff66");
}

function test(data) {
	//alert(data);
	var data = JSON.parse(data);
//	var nodedic = data.node;
//	var edgedic = data.edge;
//	neuNum += nodedic.length;
//	for(i = 0; i < nodedic.length; i++){
//		neu = nodedic[i];
//		c = "";
//		if(neu.area == "IPS"){
//			c = color[0];
//		}
//		else if(neu.area == "NMSM"){
//			c = color[1];
//		}
//		else if(neu.area == "TMSM"){
//			c = color[2];
//		}
//		
//	}
	addNodesandLinks(data);
}

function update() {
    link = vis.selectAll("line")
            .data(links, function (d) {
                return d.source.id + "-" + d.target.id;
            });

    link.enter().append("line")
            .attr("id", function (d) {
                return d.source.id + "-" + d.target.id;
            })
            .attr("stroke-width", function (d) {
                return d.value / 20;
            })
            .style("stroke","#efa9ae")
            .attr("class", "link");
    
    link.append("title")
            .text(function (d) {
                return d.weight;
            });
    link.exit().remove();

    node = vis.selectAll("g.node")
            .data(nodes, function (d) {
                return d.id;
            });

    nodeEnter = node.enter().append("g")
            .attr("class", "node")
            .call(force.drag);

    nodeEnter.append("svg:circle")
            .attr("r", function (d){
            	if(d.area == "IPS" || d.area == "Composer" || d.area == "Genre") return 18;
            	else return 10;
            })
            .attr("id", function (d) {
                return d.id;
            })
            .attr("class", "nodeStrokeClass")
            .attr("fill", function(d) { 
            	if(d.area == "IPS") return "#a9927d";
            	else if(d.area == "NMSM") return "#157f1f";
            	else if(d.area == "TMSM") return "#92140c";
            	else if(d.area == "Composer") return "#9e7682"
            	else if(d.area == "Genre") return "#a9bcd0";});

    nodeEnter.append("svg:text")
            .attr("class", "textClass")
            .attr("x", 14)
            .attr("y", ".31em")
            .style("fill","#FFFFFF")
            .style("stroke","#FFFFFF")
            .text(function (d) {
                return d.label;
            });

    node.exit().remove();

    force.on("tick", function () {
        node.attr("transform", function (d) {
            return "translate(" + d.x + "," + d.y + ")";
        });

        link.attr("x1", function (d) {
            	return d.source.x;})
            .attr("y1", function (d) {
            	return d.source.y;})
            .attr("x2", function (d) {
            	return d.target.x;})
            .attr("y2", function (d) {
            	return d.target.y;});
    });

    // Restart the force layout.
    force
            .gravity(.01)
            .charge(-8000)
            .friction(0)
            .linkDistance( function(d) { return 400;} )
            .size([w, h])
            .start();
}
function findNode(index){
	for(var i in nodes){
		if(nodes[i].id == index) return nodes[i];
	}
}
function addNodesandLinks(data) {
	for(var i = 0; i <data.node.length; i++){
		nodes.push(data.node[i]);
		update();
	}
	for(var i = 0; i < data.edge.length;i++){
		links.push({"source":findNode(data.edge[i].source),
			"target":findNode(data.edge[i].target),
			"weight":data.edge[i].weight
		});
		update();
	}
	
}

function EpisodeRecall(){
	var str = "74,72,71,72,76";
	//var str = episode.join(',');
	alert(str);
	$.get("http://localhost:8888/midicontrol",{State:"EpisodeRecall",NoteID:str},function(data,status){
		//g_data = data;
		//ips_show(data);
	})
	episode = [];
}

function PlayMidi(){
	t = flag%2;
	flag++;
	$.get("http://localhost:8888/midicontrol",{State:"Play",Flag:t},function(data,status){
		//g_data = data;
		//ips_show(data);
	})
	
}