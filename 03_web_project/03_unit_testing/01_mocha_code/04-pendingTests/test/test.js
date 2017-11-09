var expect = require('chai').expect;
var example = require('../index');

describe('test suite', function () {
	var result = example.sayHello();
	
	it('test-case 1');
	
	it('test-case 2', function () {
		expect(result).equal('hello world');
	});
	
	it.skip('test-case 3', function () {
		expect(result, 'result type').to.be.an('string');
	});
});
