(function (module) {

    module.config(function ($stateProvider, $urlRouterProvider, $interpolateProvider) {

        $urlRouterProvider.when('/admin', '/admin/dashboard');
        $urlRouterProvider.when('/', '/admin/mobile-users');
        $urlRouterProvider.otherwise('/');

        $interpolateProvider.startSymbol('{[{');
        $interpolateProvider.endSymbol('}]}');

        $stateProvider
            .state('admin.dashboard', {
                url: '/dashboard',
                templateUrl: '/static/templates/partials/admin/messages.html',
                controller: 'MessageController'
            })

            .state('admin', {
                url: '/admin',
                templateUrl: '/static/templates/admin-panel.html'
            })

            .state('admin.mobile-users', {
                url: '/mobile-users',
                data: { pageTitle: 'Users'},
                templateUrl: '/static/templates/partials/admin/mobile-users.html',
                controller: 'MobileUserController'
            })

            .state('admin.disasters', {
                url: '/disasters',
                data: { pageTitle: 'Disasters'},
                templateUrl: '/static/templates/partials/admin/disasters.html',
                controller: 'DisastersController'
            })

            .state('admin.messages', {
                url: '/messages',
                data: { pageTitle: 'Messages'},
                templateUrl: '/static/templates/partials/admin/messages.html',
                controller: 'MessageController'
            })
    });

    module.run(function ($rootScope, $state, $stateParams) {
        $rootScope.$state = $state;
        $rootScope.$stateParams = $stateParams;
    });

})(angular.module('dms', ['ui.router', 'siTable', 'checklist-model', 'dms.message', 'dms.location', 'dms.mobile-user',
    'dms.utils', 'dms.disaster', 'dms.disaster-type']));
