//流的方式
var fs = require('fs');

var stream = fs.createReadStream('./test_file.txt');

var buf = [];
stream.on('data', function(d) {
	buf.push(d);
	console.log('ddd:', d);
});

stream.on('end', function () {
	console.log(buf.toString());
});


console.log("jdk");