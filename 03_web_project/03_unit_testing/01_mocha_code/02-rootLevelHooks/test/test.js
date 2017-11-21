var expect = require('chai').expect;
var example = require('../index');

describe('test suite 1', function () {
	it('test-case 1', function () {
		console.log(new Date() + 'test suite 1 -> test-case 1');
		var result = example.sayHello();
		expect(result).to.equal('hello world');
	});
});
