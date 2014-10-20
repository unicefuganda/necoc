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
        var processAllPolls = function(){
            PollResponsesService.all().then(function (response) {
                $scope.poll_responses = response.data;
                $scope.poll_text = 'All Poll';
            });
        };

        if (poll_id) {
            PollResponsesService.filter('poll', poll_id).then(function (response) {
                $scope.poll_responses = response.data;
                $scope.poll_text = $scope.poll_responses[0].poll.name
            });
        } else {
            processAllPolls();
        }

        $scope.backToPolls = function () {
            $state.go('admin.polls');
        };

        $scope.allPollResponses = function () {
            processAllPolls();
        };
    });

})(angular.module('dms.poll-responses', ['dms.config', 'ui.router']));
