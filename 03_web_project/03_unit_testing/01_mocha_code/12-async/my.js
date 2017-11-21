var Promise = require("bluebird");

var helloWorldAsync = Promise.resolve('hello, world');

helloWorldAsync
    .then( (data) => { 
        console.log(data); 
        return Promise.reject(30);
    })
    .tap( (num) => {
        const sum = num + 1;
        console.log(sum);
        Promise.reject(new Error('my new Error'));
    })
    .then( console.log)
    .catch(console.error);

