(function (module) {

    module.factory('MobileUserService', function ($http, Config) {
        return {
            create: function (user) {
                return $http.post(Config.apiUrl + 'mobile-users/', user);
            },
            all: function () {
                return $http.get(Config.apiUrl + 'mobile-users/');
            }
        };
    });

    module.controller('MobileUserController', function ($scope, MobileUserService) {
        $scope.users = [];

        MobileUserService.all().then(function (response) {
            $scope.users = response.data;
        });
    });

    module.controller('MobileUserModalController', function ($scope, MobileUserService) {
        $scope.saveUser = function (user) {
            if ($scope.mobile_user_form.$valid) {
                $scope.saveStatus = true;

                MobileUserService.create(user)
                    .then(function (response) {
                        $scope.saveStatus = false;
                        $scope.user = null;
                        $scope.hasErrors = false;
                        $scope.users.push(response.data);
                    }, function (error) {
                        $scope.errors = error.data;
                        invalidate($scope.mobile_user_form, $scope.errors);
                        $scope.saveStatus = false;
                        $scope.hasErrors = true;
                    });

            } else {
                $scope.hasErrors = true;
            }
        };


        function invalidate(form, errors) {
            Object.keys(errors).forEach(function (key) {
                form[key].$invalid = true;
            });
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


})(angular.module('dms.mobile-user', ['dms.config']));