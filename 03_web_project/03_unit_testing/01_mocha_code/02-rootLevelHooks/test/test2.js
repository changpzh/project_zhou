var expect = require('chai').expect;
var example = require('../index');

describe('test suite 2', function () {
	it('test-case 1', function () {
		console.log(new Date() + 'test suite 2 -> test-case 1');
		var result = example.sayHello();
		expect(result).equal('hello world');
	});
});
