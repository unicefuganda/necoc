(function (module) {

    module.factory('MobileUserService', function ($http, Config) {
        return {
            create: function (user) {
                return $http.post(Config.apiUrl + 'mobile-users/', user);
            },
            all: function () {
                return $http.get(Config.apiUrl + 'mobile-users/');
            },
            update:function (user) {
                return $http.post(Config.apiUrl + 'mobile-users/' + user.id + '/', user);
            }
        };
    });

    module.controller('MobileUserController', function ($scope, $state, MobileUserService) {
        $scope.users = [];

        MobileUserService.all().then(function (response) {
            $scope.users = response.data;
        });

        $scope.showUserProfile = function (user) {
            $state.go('admin.user', {'user': user.id});
        }
    });

    module.controller('AddUserController', function ($scope, MobileUserService, helpers) {
        $scope.user = {}
        $scope.saveUser = function (user) {
            if ($scope.user_form.$valid) {
                $scope.saveStatus = true;
                MobileUserService.create(user)
                    .then(function (response) {
                        $scope.saveStatus = false;
                        $scope.user = null;
                        $scope.hasErrors = false;
                        $scope.users.push(response.data);
                    }, function (error) {
                        $scope.errors = error.data;
                        helpers.invalidate($scope.user_form, $scope.errors);
                        $scope.saveStatus = false;
                        $scope.hasErrors = true;
                    });

            } else {
                $scope.hasErrors = true;
            }
        };
    });

    module.controller('EditUserController', function ($scope, MobileUserService, helpers) {
        $scope.editUser = function (user) {
            if ($scope.user_form.$valid) {
                $scope.saveStatus = true;
                delete user.username;
                MobileUserService.update(user)
                    .then(function (response) {
                        $scope.saveStatus = false;
                        $scope.profile = response.data;
                        $scope.hasErrors = false;
                    }, function (error) {
                        $scope.errors = error.data;
                        $scope.saveStatus = false;
                        helpers.invalidate($scope.user_form, $scope.errors);
                        $scope.hasErrors = true;
                    });

            } else {
                $scope.hasErrors = true;
            }
        }
    });

    module.directive('recipients', function (MobileUserService) {
        return {
            link: function (scope, element) {
                var $select = element.selectize({
                    persist: false,
                    valueField: 'phone',
                    labelField: 'name',
                    searchField: ['name', 'phone'],
                    maxItems: null,
                    create: true,
                    preload: true,
                    createOnBlur: true,
                    load: function (query, callback) {
                        MobileUserService.all().then(function (response) {
                            callback(response.data);
                        });
                    },
                    render: {
                        item: function (item, escape) {
                            return '<div>' +
                                (item.name ? '<span class="name">' + escape(item.name) + '</span>' : '') +
                                (item.phone ? '<span class="phone">' + escape(item.phone) + '</span>' : '') +
                                '</div>';
                        },
                        option: function (item, escape) {
                            var label = item.name || item.phone;
                            var caption = item.phone ? item.phone : null;
                            var location = item.location.name ? item.location.name : null;
                            return '<div>' +
                                '<span class="list-label">' + escape(label) + '</span>' +
                                (location ? '<span class="location">' + escape(location) + '</span>' : '') +
                                (caption ? '<span class="caption">' + escape(caption) + '</span>' : '') +
                                '</div>';
                        }
                    }
                });

                scope.$watch('sms', function (sms) {
                    if (!sms) {
                        var selectize = $select[0].selectize;
                        selectize.clear();
                    }
                });
            }
        }
    });

    module.directive('buttonSwitch', function () {
        return {
            link: function (scope, element, attrs) {
                var onText = attrs.on,
                    offText = attrs.off,
                    sectionIdToToggle = attrs.toggleSection;

                element.html('<a class="btn btn-xs btn-default">' + onText + '</a>' +
                    '<a class="btn btn-xs btn-primary active">' + offText + '</a>');

                element.find('.btn').click(function () {
                    element.find('.btn').toggleClass('active');
                    element.find('.btn').toggleClass('btn-primary');
                    element.find('.btn').toggleClass('btn-default');
                    console.log($('#' + sectionIdToToggle));
                    $('#' + sectionIdToToggle).toggleClass('hide');
                });
            }
        }
    });

})(angular.module('dms.mobile-user', ['dms.config', 'dms.utils']));