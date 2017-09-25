function httpGet(url) {
    return new Promise(
        function (resolve, reject) {
            const request = new XMLHttpRequest();
            request.onload = function () {
                if (this.status === 200) {
                    // Success
                    resolve(this.response);
                } else {
                    // Something went wrong (404 etc.)
                    reject(new Error(this.statusText));
                }
            };
            request.onerror = function () {
                reject(new Error(
                    'XMLHttpRequest Error: '+this.statusText));
            };
            request.open('GET', url);
            request.send();
        });
}

// function httpGetNew(url) {
//     const request = new XMLHttpRequest();
//     request.onload = function () {
//         return (this.status === 200) ? Promise.resolve(this.response) : Promise.reject(new Error(this.statusText))
//     };
//
//     request.onerror = function () {
//         return Promise.reject(new Error('XMLHttpRequest Error: ' + this.statusText));
//     };
//
//     request.open('GET', url);
//     request.send();
// }

httpGet('http://example.com/file.txt')
    .then(
        function (value) {
            console.log('Contents: ' + value);
        },
        function (reason) {
            console.error('Something went wrong', reason);
        });