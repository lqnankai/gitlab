var url = "ws://localhost:61614/stomp";
var login = 'admin';
var passcode = 'admin';
var destination = "/Queue/SampleQueue";
client = Stomp.client(url);

var onconnect = function(frame) {
	client.subscribe(destination,function(message){
		//console.log(message.body);
		test(message.body);
		//setTimeout(after,10000);
	});
};

client.connect(login,passcode,onconnect);


