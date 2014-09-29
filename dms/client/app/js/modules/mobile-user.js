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


})(angular.module('dms.mobile-user', ['dms.config']));