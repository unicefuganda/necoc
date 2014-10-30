(function (module) {

    module.config(function ($stateProvider, $urlRouterProvider, $interpolateProvider) {

        $urlRouterProvider.when('/admin', '/admin/dashboard');
        $urlRouterProvider.when('/', '/admin/dashboard');
        $urlRouterProvider.otherwise('/');

        $interpolateProvider.startSymbol('{[{');
        $interpolateProvider.endSymbol('}]}');

        $stateProvider
            .state('admin.dashboard', {
                url: '/dashboard',
                data: { pageTitle: 'Dashboard' },
                templateUrl: '/static/templates/partials/admin/dashboard.html'
            })

            .state('admin.dashboard.district', {
                url: '/:district',
                data: { pageTitle: 'Dashboard'},
                templateUrl: '/static/templates/partials/admin/dashboard.html'
            })

            .state('admin.dashboard.district.subcounty', {
                url: '/:subcounty',
                data: { pageTitle: 'Dashboard'},
                templateUrl: '/static/templates/partials/admin/dashboard.html'
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

            .state('admin.polls', {
                url: '/polls',
                data: { pageTitle: 'Polls'},
                templateUrl: '/static/templates/partials/admin/polls.html',
                controller: 'PollsController'
            })

            .state('admin.poll-responses', {
                url: '/poll-responses/:poll',
                data: { pageTitle: 'Poll Responses'},
                templateUrl: '/static/templates/partials/admin/poll-responses.html',
                controller: 'PollResponsesController'
            })

            .state('admin.disasters', {
                url: '/disasters',
                data: { pageTitle: 'Disasters'},
                templateUrl: '/static/templates/partials/admin/disasters/disasters.html',
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
        $rootScope.params = {location : $stateParams};
    });

})(angular.module('dms', ['ui.router', 'siTable', 'checklist-model', 'dms.message', 'dms.admin-panel', 'dms.location', 'dms.mobile-user',
    'dms.utils', 'dms.disaster', 'dms.disaster-type', 'dms.map', 'dms.polls', 'dms.poll-responses', 'dms.filters', 'dms.dashboard']));
