if(currentState == "Remember"){
		order = order +1;
		$.get("http://localhost:8888/musiccontrol",{action:"16",name:MusicName,count:order},function(data,status)
		{
			msm_show(data);
		});	
	}