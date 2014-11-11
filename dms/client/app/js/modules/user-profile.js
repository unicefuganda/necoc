(function (module) {

    module.factory('UserProfileService', function ($http, Config) {
        return {
            profile: function (user_id) {
                return $http.get(Config.apiUrl + 'mobile-users/' + user_id + '/');
            }
        };
    });

    module.controller('UserProfileController', function ($scope, UserProfileService, $stateParams) {
        var userId = $stateParams.user;
        UserProfileService.profile(userId).then(function (response) {
            $scope.profile = response.data;
            $scope.user = angular.copy($scope.profile);
        });
        $scope.onEdit = true;
    });

})(angular.module('dms.user-profile', ['dms.config']));