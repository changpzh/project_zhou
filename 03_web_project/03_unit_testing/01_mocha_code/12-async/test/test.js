var expect = require('chai').expect;
var example = require('../index');
var Promise = require('bluebird');

describe('test suite', function () {
	it('test-case 1', function (done) {
		console.log(new Date() + 'test-case 1 begining...');
		Promise.resolve(example.sayHello())
            .then((result) => {
                cosole.log('in then path');
                console.log(new Date() + 'test-case 1 resolve');
                expect(result, 'result type').equal('hello world');
                done();
            })
            .catch ((e) => {
                console.log('in catch path');
                console.log(new Date() + e.message);
                done();
		});
	});
});
