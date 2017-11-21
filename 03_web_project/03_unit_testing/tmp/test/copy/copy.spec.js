const expect = require('chai').expect;
const copy = require('../copy');

describe('suite copy', () => {
    let suite;

    //beforEach
    beforeEach( () => {
        suite = {};
        suite.resObj = {'a': 'zhou', b: [2,3,5]};
        suite.resArray = [2,'changping', 4];
        suite.numZero = 0;
    });

    //afterEach
    afterEach( () => {
        suite = null; 
    });

    it('deepCopyIfNeeded: ->firstArg:object, secArg:undefined/noneExists', () => {
        const results = copy.deepCopyIfNeeded(suite.resObj); 

        expect(results).to.equal(suite.resObj);

    });
    
    it('deepCopyIfNeeded: ->firstArg:object, secArg: Boolean(true)', () => {
        const result = copy.deepCopyIfNeeded(suite.resObj, true);

        expect(result).to.not.equal(suite.resObj);
        expect(result).to.be.a('object');
    });

    it('deepCopyIfNeeded: ->firstArg:object, secArg: Boolean(false)', () => {
        const result = copy.deepCopyIfNeeded(suite.resObj, false);

        expect(result).to.equal(suite.resObj);
    });

    it.skip('deepCopyIfNeeded: ->firstArg:Object, secArg: NotBoolean(numZero)', () => {
        //const newErr = new Error(`paras:returnSafeRef can be ignored, otherwise, must be boolean value\(true, false\)!\nYour secArg is: ${suite.numZero}`);
        const newErr = new Error(`paras error`);
        console.log(copy.deepCopyIfNeeded(suite.resObj, suite.numZero));
        //expect(copy.deepCopyIfNeeded(suite.resObj,suite.numZero)).to.throw(newErr);
    });
    
    it('deepCopy: arg:Array', () => {
        expect(copy.deepCopy(suite.resArray)).to.not.equal(suite.resArray);
    });

    it('deepCopy: arg: undefined', () => {
        expect(copy.deepCopy(undefined)).to.equal(undefined);
    });
});
