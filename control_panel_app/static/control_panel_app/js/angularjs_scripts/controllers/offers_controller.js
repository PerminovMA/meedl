/**
 * Created by Mihail on 10.03.15.
 */

app.controller('OffersController', function ($scope, $http) {

    $http({method: 'GET', url: '/rest_api/offers/', cache: true}).
        success(function (data, status) {
            $scope.offers_list = data;
        }).
        error(function (data, status) {
            alert("Connection error! Cant get offers. Status request: " + status);
        });

});