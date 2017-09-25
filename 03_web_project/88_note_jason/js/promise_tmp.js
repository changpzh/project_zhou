// import {readFile} from 'fs';

var fs = require('fs');

function readFilePromisified(filename) {
    return new Promise(
        function (resolve, reject) {
            fs.readFile(filename, { encoding: 'utf8' },
                (error, data) => {
                if (error) {
                    reject(error);
                } else {
                    resolve(data);
                }
            });
        });
}

readFilePromisified(process.argv[2])
    .then(text => {
    console.log(text);
})
.catch(error => {
    console.log(error);
});