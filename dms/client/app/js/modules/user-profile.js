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
            var randomCacheBustingParam = '?decache=' + Math.floor(Math.random() * 10000000000);
            $scope.profileImageSrc = '/api/v1/photo/' + response.data.id + randomCacheBustingParam;
        });
        $scope.onEdit = true;

        $scope.setProfile = function (profile) {
            $scope.profile  = profile
            var randomCacheBustingParam = '?decache=' + Math.floor(Math.random() * 10000000000);
            $scope.profileImageSrc = '/api/v1/photo/' + profile.id + randomCacheBustingParam;
        }
    });

})(angular.module('dms.user-profile', ['dms.config']));