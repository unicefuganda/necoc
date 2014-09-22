(function (module) {

    module.config(function ($routeProvider, $interpolateProvider, $locationProvider) {
        $locationProvider.html5Mode(true);

        $interpolateProvider.startSymbol('{[{');
        $interpolateProvider.endSymbol('}]}');

        $routeProvider
            .when('/', {
                templateUrl: '/static/templates/messages.html',
                controller: 'MessageController'
            })
            .otherwise({
                redirectTo: '/'
            });

    });

})(angular.module('dms', ['ngRoute', 'dms.message']));
