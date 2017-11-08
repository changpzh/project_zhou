var Promise = require("bluebird");

function hello() {
	throw 'test error';
}

function sayHello() {
	return hello().then(function(result){
		return result;
	});
}

function sayHelloTry() {
	return Promise.try(function() {
		return hello();
	}).then(function(result){
		return result;
	});
}

module.exports.sayHello = sayHello;
module.exports.sayHelloTry = sayHelloTry;
