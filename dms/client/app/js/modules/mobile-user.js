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

        $scope.saveUser = function (user) {
            $scope.saveStatus = true;

            MobileUserService.create(user)
                .then(function (response) {
                    $scope.saveStatus = false;
                    $scope.users.push(response.data);
                });
        };

        MobileUserService.all().then(function (response) {
            $scope.users = response.data;
        });
    });

})(angular.module('dms.mobile-user', ['dms.config']));