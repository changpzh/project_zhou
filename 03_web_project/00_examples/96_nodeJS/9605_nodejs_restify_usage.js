var restify = require('restify');
var server = restify.createServer({
    name: 'myApp',
    version: '1.0.0'
});

server.get('/:params/abc', function (req, res, next) {
    console.warn('warnging->', req.params['params']);
    console.error('error->', req.params['params']);
    console.log('log->', req.params['params']);
    res.send({a:23, b: 2});
    return next();
});

server.get(/.*/, restify.serveStatic ({
    directory: 'public/',
    default: 'index.html'
}));

//server.listen(9091, 'localhost', function () {
server.listen(9091, function () {
    console.log('%s listening at %s', server.name, server.url);
});