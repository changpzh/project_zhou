var fs = require('fs'); //node js related files
var event = require('events'); //let you use async data.
var newEvent = new event.EventEmitter();

var result = '';

newEvent.on('data is ready', function () {
	console.log("newEvent called and result: ", result.toString()	);
});

fs.readFile('./test_file.txt', function(err, data) {
	console.log("zzz");
	console.log("data:\n", data.toString());

	newEvent.emit('data is ready'); //throw a message when you want to excute anther code.

});

console.log("jak");