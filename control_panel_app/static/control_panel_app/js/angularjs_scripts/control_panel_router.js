/**
 * Created by PerminovMA@live.ru on 08.03.15.
 */

app.config(function ($routeProvider) {
    $routeProvider
        .when('/', {
            templateUrl: '/static/control_panel_app/pages/test1.html',
            controller: 'RepsListController'
        })
        .when('/campaigns', {
            templateUrl: '/control_panel/campaigns',
            controller: 'CampaignsController'
        })
        .when('/create_campaign', {
            templateUrl: '/control_panel/create_campaign',
            controller: 'CreateCampaignsController'
        })
        .otherwise({
            redirectTo: '/'
        });
});

app.controller('RepsListController', function ($scope) {
    $scope.name = "Mihail";
});

app.controller('CreateCampaignsController', function ($scope) {
    $scope.name = "Mihail";
});