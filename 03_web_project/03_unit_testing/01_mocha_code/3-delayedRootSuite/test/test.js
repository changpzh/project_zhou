var expect = require('chai').expect;
var example = require('../index');

describe('test suite', function () {
	var result = example.sayHello();
	
	beforeEach(function (done) {
		console.log(new Date() + 'test suite before each');
		setTimeout(done, 1000);
	});
	
	it('test-case 1', function () {
		console.log(new Date() + 'test-case 1');
		expect(result, 'result type').to.be.an('string');
	});
	
	it('test-case 2', function () {
		expect(result).equal('hello world');
	});
});
