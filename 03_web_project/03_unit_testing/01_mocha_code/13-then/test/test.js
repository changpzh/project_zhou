var expect = require('chai').expect;
var example = require('../index');
var Promise = require('bluebird');

describe('test suite', function () {
	it('test-case 1', function (done) {
		console.log(new Date() + 'test-case 1');
		example.sayHello().then(function (result) {
			console.log(new Date() + 'test-case 1 resolve');
			expect(result, 'result').equal('hello world');
		}, function (result) {
			console.log(new Date() + 'test-case 1 reject');
			expect(result, 'result').equal('hello world');
		})
		.finally(function(){
			done();
		});		
	});
});
