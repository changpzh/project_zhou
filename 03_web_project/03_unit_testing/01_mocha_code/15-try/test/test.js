var expect = require('chai').expect;
var example = require('../index');
var Promise = require('bluebird');

describe('test suite', function () {
	it('test-case 1', function (done) {
	/* 	example.sayHello().then(function(){},function(result){
			console.log(result);
			done();
		});  */
		
		example.sayHelloTry().then(function(){},function(result){
			console.log(result);
			done();
		}); 
	});
});