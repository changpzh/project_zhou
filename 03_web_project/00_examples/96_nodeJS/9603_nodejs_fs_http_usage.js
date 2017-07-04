//Http server of nodejs, while 处理文件比较大的时候

var http = require('http');
var fs = require('fs');

http.createServer(function(req, res) {
	console.log("%j", req);
	var stream = fs.createReadStream('./test.txt');
	stream.pipe(res);
}).listen(4034); //port