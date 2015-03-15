/**
 * Created by PerminovMA@live.ru on 08.03.15.
 */

var app = angular.module('control_panel_angular_module', ['ngRoute', 'ngResource']);

app.config(function ($interpolateProvider) {
    //allow django templates and angular to co-exist
    $interpolateProvider.startSymbol('{[{');
    $interpolateProvider.endSymbol('}]}');
});

// URLs config
app.constant("urls", {detail_campaign_url: "/control_panel/detail_campaign/"});