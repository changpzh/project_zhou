var Promise = require("bluebird");
var fs = Promise.promisifyAll(require("fs"));

fs.readdirAsync(process.cwd())
    .tap(console.log)
    .tap((files) => {
        files.filter(fileName => {
            return fs.statAsync(fileName)
                .then( stat => stat.isFile())
                .catch( () => false);
        })
        .forEach(fileName => {console.log(`${fileName} is a file!`)})
    })
    .filter((fileName) => 
        fs.statAsync(fileName)
            .then((stat) => stat.isDirectory())
            .catch(() => false)
    )
    .tap(console.log)
    .each((directoryName) => {
        console.log(directoryName, " is an accessible directory");
    });
