var expect = require('chai').expect;
var example = require('../index');

describe('test suite', function () {
	var result = example.sayHello();
	
	it('test grep 1', function () {
		expect(result, 'result type').to.be.an('string');
	});
	
	it('test-grep 2', function () {
		expect(result).equal('hello world');
	});
});
