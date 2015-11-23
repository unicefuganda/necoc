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
        $scope.onEdit = true;
        var msg_sender = '';

        this.showProfile = function(profile_id) {
            $scope.$apply( function() {
                msg_sender = profile_id;
                UserProfileService.profile(msg_sender).then(function (response) {
                    $scope.setProfile(response.data);
                 });
            });
        }
        $scope.showProfile = this.showProfile;

        $scope.setProfile = function (profile) {
            $scope.profile  = profile;
            $scope.user = angular.copy($scope.profile);
            var randomCacheBustingParam = '?decache=' + Math.floor(Math.random() * 10000000000);
            $scope.profileImageSrc = '/api/v1/photo/' + profile.id + randomCacheBustingParam;
        }
        if (userId) {
            UserProfileService.profile(userId).then(function (response) {
                $scope.setProfile(response.data);
            });
        }
    });

})(angular.module('dms.user-profile', ['dms.config']));