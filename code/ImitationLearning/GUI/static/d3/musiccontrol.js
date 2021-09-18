var currentState = "None";
var episodeRecallState = false;
var MusicName = "";
var order = 0;
var msg = "";
var episodeNotes = "";
var flag = true;
var epiRecallNotes={};
var lastPlayTime = 0;
var notes = "";
var intervals = "";
function MusicLearning() {
	$("#music").css("background-color","F08080");
	$("#music").css("border-bottom","1px solid F08080");
	$("#music").css("border-left","1px solid F08080");
	$("#music").css("border-right","1px solid F08080");
	//$("#GoalName").text("Music");
	
	$("#goal").val("Rain");
}

function play(key) {
	var audio = document.getElementById("keymp3");
	urls = "/static/notes/"+key.toString() + ".mp3";
	audio.src = urls;
	audio.play();
}

function RecallPlay(notes,i) {
	var len = (Object.keys(notes).length);
	if(i > len){flag = true;}
	else {
		var audio = document.getElementById("keymp3");
		var key = notes[i];
		id = key["id"];
		urls = "/static/notes/"+id.toString()+ ".mp3";
		audio.src = urls;
		audio.play();
		console.log(audio.src);
		audio.onended = function() {
			RecallPlay(notes,i+1);
		}
	}
}
function playkey_old(key) {
	play(key);
	var myTime = new Date()
	alert(myTime.getTime());
	if(episodeRecallState == true) 
		episodeNotes += key.toString() + ",";
	if(currentState == "Remember"){
		order = order +1;
		$.get("http://localhost:8888/musiccontrol",{action:key,name:MusicName,count:order},function(data,status)
		{
			msm_show(data);
		});	
	}
}

function playkey(key) {
	var myTime = new Date();
	var t = myTime.getTime();
	play(key);
	if(episodeRecallState == true) 
		episodeNotes += key.toString() + ",";
	if(currentState == "Remember"){
		order = order +1;
		var Interval = 0;
		if(order > 1){
			Interval = t - lastPlayTime;
			intervals += Interval.toString() + ",";
		}
		notes += key.toString() + ",";
//		$.get("http://localhost:8888/musiccontrol",{action:key,name:MusicName,count:order,interval:Interval},function(data,status)
//		{
//			msm_show(data);
//		});
		lastPlayTime = t
	}
}

function StopPlay() {
	var myTime = new Date();
	var t = myTime.getTime();
	var Interval = t - lastPlayTime;
	intervals += Interval.toString() + ",";
	alert(intervals);
	
	if(currentState == "Remember"){
		$.get("http://localhost:8888/musiccontrol",{action:notes,name:MusicName,interval:intervals},function(data,status)
				{
					msm_show(data);
				});
	}
}

function Remember() {
	$("#rtable").empty();
	$("#resultnotes").empty();
	currentState = "Remember";
	order = 0;
	notes = "";
	intervals = "";
	MusicName = $("#goal").val();
	if(MusicName == "") {
		alert("Please input the Music Name!")
	}
	else{
		$.get("http://localhost:8888/play",{State:currentState,goalname:MusicName},function(data,status){
			ips_show(data);
		})
	}
}

function Recall() {
	currentState = "Recall";
	order = 0;
	MusicName = ""
	var musicname = $("#goal").val();
	if(musicname == "") {
		alert("Please input the Music Name!")
	}
	else{
		$.get("http://localhost:8888/play",{State:currentState,goalname:musicname},function(data,status){
			notes = JSON.parse(data);
			console.log(notes);
			len = (Object.keys(notes).length);
			msg = "";
			//alert("hh");
			RecallPlay(notes,1);
			for(var i = 1; i <= len; i++) {
				n = notes[i];
				name = n.name
				msg += name.toString() + " ";
				$("#resultnotes").text(msg);
			}
			
		})
	}
}
function Recall2() {
	$("#rtable").empty();
	$("#resultnotes").empty();
	currentState = "Recall";
	if(episodeRecallState == false) {
		order = 0;
		MusicName = ""
		var musicname = $("#goal").val();
		if(musicname == "") {
			alert("Please input the Music Name!")
		}
		else{
			$.get("http://localhost:8888/play",{State:currentState,goalname:musicname,episode:""},function(data,status){
				notes = JSON.parse(data);
				console.log(notes);
				len = (Object.keys(notes).length);
				msg = "";
				//alert("hh");
				RecallPlay(notes,1);
				for(var i = 1; i <= len; i++) {
					n = notes[i];
					name = n.name
					msg += name.toString() + " ";
					$("#resultnotes").text(msg);
				}
				
			})
		}
	}
	else {
		if(episodeNotes.length == 0) alert("please play an episode of music!");
		else {
			$.get("http://localhost:8888/play",{State:"EpisodeRecall",goalname:"",episode:episodeNotes},function(data,status){
				
				//episodeResultProcess(data);
				createResultTable(data);
				episodeRecallState = false;
				episodeNotes = "";
			})
			
		}
	}
	
}

function createResultTable(data) {
	if(episodeRecallState == true){
		var title=["song","Notes you played","Rest Notes","Listen"]
		var table = $("#rtable");
		var tr=$("<tr></tr>");
		var cellCount = 4;
		tr.appendTo(table);
		for(var i=0;i < cellCount; i++){
			var td=$("<td>"+title[i]+"</td>");
			td.css("color","#FFE473");
			td.appendTo(tr);
		}
		//alert(data);
		var results = JSON.parse(data);
		len = (Object.keys(results).length);
		for(var i=0;i<len;i++){
			var row = $("<tr></tr>");
			row.appendTo(table);
			
			res = results[i];
			//first column:Goal name
			var goaltd = $("<td>"+res.goal+"</td>");
			goaltd.appendTo(row);
			
			//second column:episode notes
			epimsg='';
			ns = {};
			epi = res.episodenotes;
			elen = (Object.keys(epi).length);
			for(var j = 1; j <= elen;j++){
				n = epi[j]
				name = n.name;
				ns[j]=n;
				epimsg += name.toString() + ' ';
			}
			var epitd = $("<td>"+epimsg+"</td>");
			epitd.appendTo(row);
			
			//third column:rest notes
			restmsg='';
			restnotes = res.rest;
			
			
			rlen = (Object.keys(restnotes).length);
			for(var j = 1;j <= rlen;j++){
				n = restnotes[j];
				console.log(n);
				name = n.name;
				ns[j+elen]=n;
				restmsg += name.toString() + ' ';
			}
			epiRecallNotes[res.goal]=ns;
			var resttd = $("<td>"+restmsg+"</td>");
			resttd.appendTo(row);
			
			//order = "<td><a onclick='test("+res.goal+")'>listen to me</td>";
			order = "<td>Listen to me</td>"
			var buttontd = $(order);
			buttontd.css("color","red");
			buttontd.css("text-decoration","underline");
			buttontd.attr("onclick","javascript:test('"+res.goal+"');");
			buttontd.appendTo(row);
		}
	}
}
function test(goal){
	notes = epiRecallNotes[goal];
	//alert(notes);
	RecallPlay(notes,1);
	
}
function NotesRecall() {
	$("#rtable").empty();
	$("#resultnotes").empty();
	currentState = "Recall";
	episodeRecallState = true;
}
function sleep(n)
{
  var start=new Date().getTime();
  while(true) if(new Date().getTime()-start>n) break;
}