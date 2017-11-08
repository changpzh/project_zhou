var expect = require('chai').expect;
var example = require('../index');

describe('test suite 1', function () {
	var result = example.sayHello();
	
	it('test-case 1', function () {
		expect(result, 'result type').to.be.an('string');
	});
	
	it('test-case 2', function () {
		expect(result).equal('hello world');
	});
});
