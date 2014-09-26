(function (module) {

    module.config(function ($stateProvider, $urlRouterProvider, $interpolateProvider, $locationProvider) {
        $locationProvider.html5Mode(true);
        $urlRouterProvider.otherwise('/');

        $interpolateProvider.startSymbol('{[{');
        $interpolateProvider.endSymbol('}]}');

        $stateProvider
            .state('index', {
                url: '/',
                templateUrl: '/static/templates/messages.html',
                controller: 'MessageController'
            })

    });

})(angular.module('dms', ['ui.router', 'siTable', 'dms.message']));
