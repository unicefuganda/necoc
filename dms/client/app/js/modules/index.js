(function (module) {

    module.config(function ($stateProvider, $urlRouterProvider, $interpolateProvider) {
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
                templateUrl: '/static/templates/admin-panel.html',
                controller: function ($state) {
                    $state.go('admin.mobile-users');
                }
            })

            .state('admin.mobile-users', {
                url: '/mobile-users',
                templateUrl: '/static/templates/partials/admin/mobile-users.html'
            })

    });

})(angular.module('dms', ['ui.router', 'siTable', 'dms.message', 'dms.location']));
