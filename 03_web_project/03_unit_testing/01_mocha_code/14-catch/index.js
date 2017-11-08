var Promise = require("bluebird");

function sayHello() {
	return new Promise(function (resolve, reject) {
		setTimeout(function () {
			reject('hello world');
		}, 1000);
	});
}

module.exports.sayHello = sayHello;
