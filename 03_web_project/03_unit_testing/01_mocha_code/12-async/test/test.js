var expect = require('chai').expect;
var example = require('../index');
var Promise = require('bluebird');

describe('test suite', function () {
	it('test-case 1', function (done) {
		console.log(new Date() + 'test-case 1');
		Promise.resolve(example.sayHello()).then(function (result) {
			console.log(new Date() + 'test-case 1 resolve');
			expect(result, 'result type').equal('hello world');
			done();
		}, function (result) {
			console.log(new Date() + 'test-case 1 reject');
			expect(result, 'result type').equal('hello world');
			done();
		})
		.catch (function (e) {
			console.log(new Date() + e);
			done();
		});
	});
});
