var fs = require('fs-extra');
var path = require('path');
// var dirPath = process.argv[2];  //directory path
// var fileType = '.'+process.argv[3]; //file extension
var files = [];
// fs.readdir(dirPath, function(err,list){
fs.readdir('.', function(err,list){
    if(err) throw err;
    for(var i=0; i<list.length; i++)
    {
        console.log(list[i]); //
    }
});

module.exports = function (n) { return n * 111 };