/**
 * Created by changpzh on 2017/7/19.
 */
app.controller('myTimeCtrl', function($scope, $interval) {
    $scope.curtTime = new Date().toLocaleString();
    $interval(function() {
        $scope.curtTime = new Date().toLocaleString();
    }, 1000);
});


app.controller('myNotesCtrl', ['$scope', '$http', '$interval', myNotesCtrlFn]);

function myNotesCtrlFn($scope, $http) {
    var files = ['04_run_cli.txt', '05_result', 'training_admin01.txt'];
    var newFiles = files.map(file => ({ name: file, content: '' }));

    angular.forEach(newFiles, (d) => {
        var url = 'notes/' + d.name;
        $http.get(url).then(function(data) {
            d.content = data.data;
        });
    });
    $scope.files = newFiles;
}


