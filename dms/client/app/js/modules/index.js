(function (module) {

    module.config(function ($stateProvider, $urlRouterProvider, $interpolateProvider) {

        $urlRouterProvider.when('/admin','/admin/mobile-users');
        $urlRouterProvider.otherwise('/');

        $interpolateProvider.startSymbol('{[{');
        $interpolateProvider.endSymbol('}]}');

        $stateProvider
            .state('index', {
                url: '/',
                templateUrl: '/static/templates/messages.html',
                controller: 'MessageController'
            })

            .state('admin', {
                url: '/admin',
                templateUrl: '/static/templates/admin-panel.html'
            })

            .state('admin.mobile-users', {
                url: '/mobile-users',
                templateUrl: '/static/templates/partials/admin/mobile-users.html',
                controller: 'MobileUserController'
            })

            .state('admin.disasters', {
                url: '/disasters',
                templateUrl: '/static/templates/partials/admin/disasters.html',
                controller: 'DisastersController'
            })
    });

})(angular.module('dms', ['ui.router', 'siTable', 'dms.message', 'dms.location', 'dms.mobile-user',
    'dms.utils', 'dms.disaster', 'dms.disaster-type']));
