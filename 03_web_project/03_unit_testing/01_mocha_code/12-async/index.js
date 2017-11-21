var Promise = require("bluebird");

function sayHello() {
	return new Promise(function (resolve, reject) {
		setTimeout(function () {
            return Promise.resolve('hello, world');
		}, 1000);
	});
}

module.exports.sayHello = sayHello;
