


function play16() {
	audio.src = "/static/notes/16.mp3";
	audio.play();
	if(currentState == "Remember"){
		order = order +1;
		$.get("http://localhost:8888/musiccontrol",{action:"16",name:MusicName,count:order},function(data,status)
		{
			msm_show(data);
		});	
	}
}

function play17() {
	audio.src = "/static/notes/17.mp3";
	audio.play();
	if(currentState == "Remember"){
		order = order +1;
		$.get("http://localhost:8888/musiccontrol",{action:"17",name:MusicName,count:order},function(data,status)
		{
			msm_show(data);
		});
	}
}

function play18() {
	audio.src = "/static/notes/18.mp3";
	audio.play();
	if(currentState == "Remember") {
		order = order +1;
		$.get("http://localhost:8888/musiccontrol",{action:"18",name:MusicName,count:order},function(data,status)
		{
			msm_show(data);
		});
	}
}

function play19() {
	audio.src = "/static/notes/19.mp3";
	audio.play();
	if(currentState == "Remember") {
		order = order +1;
		$.get("http://localhost:8888/musiccontrol",{action:"19",name:MusicName,count:order},function(data,status)
		{
			msm_show(data);
		});
	}
}

function play20() {
	audio.src = "/static/notes/20.mp3";
	audio.play();
	if(currentState == "Remember"){
		order = order +1;
		$.get("http://localhost:8888/musiccontrol",{action:"20",name:MusicName,count:order},function(data,status)
		{
			msm_show(data);
		});
	}
	
}

function play21() {
	audio.src = "/static/notes/21.mp3";
	audio.play();
	if(currentState == "Remember"){
		order = order +1;
		$.get("http://localhost:8888/musiccontrol",{action:"21",name:MusicName,count:order},function(data,status)
		{
			msm_show(data);
		});
	}
}

function play22() {
	audio.src = "/static/notes/16.mp3";
	audio.play();
	if(currentState == "Remember"){
		order = order +1;
		$.get("http://localhost:8888/musiccontrol",{action:"Si",name:MusicName,count:order},function(data,status)
		{
			msm_show(data);
		});
	}
}