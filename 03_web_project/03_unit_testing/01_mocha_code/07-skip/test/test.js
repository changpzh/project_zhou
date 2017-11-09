var expect = require('chai').expect;
var example = require('../index');

describe('test suite', function () {
	var result = example.sayHello();
	
	it.skip('test-case 1', function () {
		expect(result, 'result type').to.be.an('string');
	});
	
	it('test-case 2', function () {
		expect(result).equal('hello world');
	});
	
	it('test-case 3', function () {
	});
});
