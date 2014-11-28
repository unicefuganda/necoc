(function (module) {

    module.config(function ($stateProvider, $urlRouterProvider, $interpolateProvider, $httpProvider) {
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';

        $urlRouterProvider.when('/admin', '/admin/dashboard');
        $urlRouterProvider.when('/', '/admin/dashboard');
        $urlRouterProvider.otherwise('/');

        $interpolateProvider.startSymbol('{[{');
        $interpolateProvider.endSymbol('}]}');

        $stateProvider
            .state('admin.dashboard', {
                url: '/dashboard',
                data: { pageTitle: 'Dashboard' },
                templateUrl: '/static/templates/partials/admin/dashboard.html',
                controller: 'DashboardController'
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
                data: {
                    pageTitle: 'Users',
                    permissions: {
                        only: ['can_manage_users']
                    }
                },
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
                url: '/poll-responses/:poll?pollName',
                data: { pageTitle: 'Poll Responses'},
                templateUrl: '/static/templates/partials/admin/poll-responses.html',
                controller: 'PollResponsesController'
            })

            .state('admin.disasters', {
                url: '/disasters',
                data: {
                    pageTitle: 'Disasters',
                    permissions: {
                        only: ['can_manage_disasters']
                    }
                },
                templateUrl: '/static/templates/partials/admin/disasters/disasters.html',
                controller: 'DisastersController'
            })

            .state('admin.disaster-info', {
                url: '/disasters/:disaster',
                data: {
                    pageTitle: 'Disaster',
                    permissions: {
                        only: ['can_manage_disasters']
                    }
                },
                templateUrl: '/static/templates/partials/admin/disasters/disaster-info.html',
                controller: 'DisasterInfoController'
            })

            .state('admin.messages', {
                url: '/messages',
                data: {
                    pageTitle: 'Messages',
                    permissions: {
                        only: ['can_manage_messages']
                    }
                },
                templateUrl: '/static/templates/partials/admin/messages.html',
                controller: 'MessageController'
            })

            .state('admin.user', {
                url: '/users/:user',
                data: { pageTitle: 'Profile'},
                templateUrl: '/static/templates/partials/admin/users/profile.html',
                controller: 'UserProfileController'
            })
    });


    module.run(function ($rootScope, $state, $stateParams, $templateCache, Permission, User, Permissions) {
        $rootScope.$state = $state;
        $rootScope.params = {location: $stateParams};

        Permissions.LIST.forEach(function (permission) {
            Permission.defineRole(permission, function () {
                return User.hasPermission(permission);
            });
        });

        $rootScope.$on('$stateChangeStart', function (event, toState) {
            if (typeof(toState) !== 'undefined') {
                $templateCache.remove(toState.templateUrl);
            }
        });

    });

})(angular.module('dms', ['ui.router', 'permission', 'siTable', 'checklist-model', 'angularFileUpload', 'dms.message', 'dms.admin-panel', 'dms.location', 'dms.mobile-user',
    'dms.utils', 'dms.disaster', 'dms.disaster-type', 'dms.map', 'dms.polls', 'dms.poll-responses', 'dms.filters', 'dms.dashboard',
    'dms.user-profile', 'dms.user', 'angularSpinner']));

