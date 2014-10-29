(function (module) {

    module.factory('PollService', function ($http, Config) {
        return {
            sendPoll: function (poll) {
                return $http.post(Config.apiUrl + 'polls/', poll);
            },
            all: function () {
                return $http.get(Config.apiUrl + 'polls/');
            }
        }
    });

    module.controller('PollsController', function ($scope, PollService, PollResponsesService, $state) {
        PollService.all().then(function (response) {
            $scope.polls = response.data;
        });

        $scope.showPollResponses = function (poll) {
            $state.go('admin.poll-responses', {poll: poll.id});
        };

    });

    module.controller('NewPollController', function ($scope, PollService, growl, helpers) {

        $scope.sendPoll = function () {
            if ($scope.new_poll_form.$valid) {
                $scope.saveStatus = true;
                $scope.poll.target_locations = helpers.stringToArray($scope.poll.target_locations, ',');

                PollService.sendPoll($scope.poll)
                    .then(function (response) {
                        $scope.saveStatus = false;
                        $scope.successful = true;
                        $scope.poll = null;
                        $scope.polls.push(response.data);
                        growl.success('Poll successfully sent', {
                            ttl: 3000
                        });
                    }, function (error) {
                        $scope.errors = error.data;
                        helpers.invalidate($scope.new_poll_form, $scope.errors);
                        $scope.saveStatus = false;
                        $scope.hasErrors = true;
                    });

            } else {
                $scope.hasErrors = true;
            }
        }
    });

})(angular.module('dms.polls', ['dms.config', 'angular-growl', 'dms.utils', 'dms.poll-responses']));
