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

    module.controller('PollResponsesController', function ($scope, PollResponsesService, $stateParams, $state, Config) {
        var poll_id = $stateParams.poll;
        $scope.export_poll_response_url = Config.exportPollUrl;

        if (poll_id) {
            PollResponsesService.filter('poll', poll_id).then(function (response) {
                $scope.poll_responses = response.data;
                $scope.poll_text = $stateParams.pollName;
                console.log($stateParams.pollName);
            });
            $scope.export_poll_response_url += poll_id + '/';
        }

        $scope.backToPolls = function () {
            $state.go('admin.polls');
        };

    });

})(angular.module('dms.poll-responses', ['dms.config', 'ui.router']));
