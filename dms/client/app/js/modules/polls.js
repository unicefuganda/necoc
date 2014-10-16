(function (module) {

    module.controller('NewPollController', function ($scope) {
        $scope.sendPoll = function () {
            if ($scope.new_poll_form.$valid) {

            } else {
                $scope.hasErrors = true;
            }
        }
    });

})(angular.module('dms.polls', ['dms.config']));
