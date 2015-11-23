(function (module) {

    module.factory('SenderService', function ($http, Config) {
        return {
            profile: function (user_id) {
                return $http.get(Config.apiUrl + 'mobile-users/' + user_id + '/');
            }
        };
    });

    module.controller('SenderProfileController', function ($scope, SenderService, $stateParams) {

        var userId = 'undefined';

        this.setModel = function(data) {
              $scope.$apply( function() {
                 $scope.userId = data;
              });
        }

        $scope.setModel = this.setModel;

        $scope.setProfile = function (profile) {
            $scope.profile  = profile;
            $scope.user = angular.copy($scope.profile);
            var randomCacheBustingParam = '?decache=' + Math.floor(Math.random() * 10000000000);
            $scope.profileImageSrc = '/api/v1/photo/' + profile.id + randomCacheBustingParam;
        }
        SenderService.profile(userId).then(function (response) {
            $scope.setProfile(response.data);
        });
    });

})(angular.module('dms.sender-profile', ['dms.config']));