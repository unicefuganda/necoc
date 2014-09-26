(function (module) {

    module.factory('MobileUserService', function ($http, Config) {
        return {
            create: function (user) {
               return $http.post(Config.apiUrl + 'mobile-users/', user);
            }
        };
    });

    module.controller('MobileUserController', function ($scope, MobileUserService) {
        $scope.users = [];

        $scope.saveUser = function (user) {
            MobileUserService.create(user)
                .then(function(response) {
                    $scope.users.push(response.data);
                });
        };
    });

})(angular.module('dms.mobile-user', ['dms.config']));