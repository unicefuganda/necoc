(function (module) {

    module.factory('PollResponsesService', function ($http, Config) {
        return {
            all: function () {
                return $http.get(Config.apiUrl + 'poll-responses/');
            },
            filter: function (filter, filter_id) {
                return $http.get(Config.apiUrl + 'poll-responses/?' + filter + '=' + filter_id);
            }
        }
    });

    module.controller('PollResponsesController', function ($scope, PollResponsesService, $stateParams, $state) {
        var poll_id = $stateParams.poll;
        if (poll_id) {
            PollResponsesService.filter('poll', poll_id).then(function (response) {
                $scope.poll_responses = response.data;
            });
        } else {
            PollResponsesService.all().then(function (response) {
                $scope.poll_responses = response.data;
            });
        }

        $scope.backToPolls = function(){
            $state.go('admin.polls');
        };
    });

})(angular.module('dms.poll-responses', ['dms.config', 'ui.router']));
