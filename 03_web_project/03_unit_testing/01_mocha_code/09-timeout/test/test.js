describe('a suite of tests', function () {
	this.timeout(200); // SUITE-LEVEL

	beforeEach(function (done) {
		this.timeout(3000); // HOOK-LEVEL
		setTimeout(done, 2500);
	});

	it('should take less than 500ms', function (done) {
		this.timeout(500); // TEST-LEVEL
		setTimeout(done, 300);
	});

	it('should take less than 200ms', function (done) {
		setTimeout(done, 250);
	});
})
