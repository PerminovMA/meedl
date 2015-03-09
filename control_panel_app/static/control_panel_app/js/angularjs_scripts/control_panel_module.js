/**
 * Created by PerminovMA@live.ru on 08.03.15.
 */

var app = angular.module('control_panel_angular_module', ['ngRoute']);

app.config(function ($interpolateProvider) {
    //allow django templates and angular to co-exist
    $interpolateProvider.startSymbol('{[{');
    $interpolateProvider.endSymbol('}]}');
});