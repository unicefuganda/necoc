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
                $scope.poll.target_locations = ($scope.poll.subcounties && $scope.poll.subcounties.length > 0) ?
                    helpers.stringToArray($scope.poll.subcounties, ',') : helpers.stringToArray($scope.poll.districts, ',');
                delete $scope.poll.districts;
                delete $scope.poll.subcounties;

                PollService.sendPoll($scope.poll)
                    .then(function (response) {
                        $scope.saveStatus = false;
                        $scope.successful = true;
                        $scope.poll = null;
                        $scope.polls.push(response.data);
                        $scope.hasErrors = false;
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
