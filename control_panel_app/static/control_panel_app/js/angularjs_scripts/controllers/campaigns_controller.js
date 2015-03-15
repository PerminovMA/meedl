/**
 * Created by Mihail on 10.03.15.
 */

app.controller('CampaignsController', function ($scope, $http, urls) {

    $scope.detail_campaign_url = urls.detail_campaign_url;  // url configuration file located in module file

    $http({method: 'GET', url: '/rest_api/adv_campaigns/', cache: true}).
        success(function (data, status) {
            $scope.adv_campaigns_list = data;
        }).
        error(function (data, status) {
            alert("Connection error! Cant get campaigns. Status request: " + status);
        });

});