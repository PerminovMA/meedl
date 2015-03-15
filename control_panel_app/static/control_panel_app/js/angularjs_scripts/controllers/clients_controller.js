/**
 * Created by Mihail on 10.03.15.
 */

app.controller('ClientsController', function ($scope, $http) {

    $http({method: 'GET', url: '/rest_api/clients/', cache: true}).
        success(function (data, status) {
            $scope.clients_list = data;
        }).
        error(function (data, status) {
            alert("Connection error! Cant get clients. Status request: " + status);
        });

});