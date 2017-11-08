var expect = require('chai').expect;
var example = require('../index');
var Promise = require('bluebird');

describe('test suite', function () {
	it('test-case 1', function (done) {
		Promise.resolve(example.sayHello()).then(function (result) {
		 return Promise.resolve('test');
		})
		.catch (function (e) {
			console.log('catch: ' + e);
			//return Promise.reject(new TypeError(e));
		})
		.catch (function (e) {
			console.log('catch part: ' + e);
			return Promise.resolve(e); 
		})
		.then(function (result) {
			console.log('resolve' + result);
		}, function (e) {
			console.log('rject' + e);
		})
		.finally(function(){
			done();
		});
	});
});
