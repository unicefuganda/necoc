(function (module) {

    module.factory('PollService', function ($http, Config) {
        return {
            sendPoll: function (poll) {
                return $http.post(Config.apiUrl + 'polls/', poll);
            },
            all: function () {
                return $http.get(Config.apiUrl + 'polls/');
            },
            downloadPoll: function(poll){
                return $http.get(Config.apiUrl + 'csv-poll/?poll='+poll)
            }
        }
    });

    module.controller('PollsController', function ($scope, PollService, PollResponsesService, $state, growl, helpers) {
        $scope.ptypes = {
            selectOptions: [
                {ptype: 'text', label: 'Free Text Poll'},
                {ptype: 'yesno', label: 'Yes/No Poll'}
                ],
            selectedOption: {ptype: 'text', label: 'Free Text Poll'}
            }

        PollService.all().then(function (response) {
            $scope.polls = response.data;
        });

        $scope.showPollResponses = function (poll) {
            $state.go('admin.poll-responses', {poll: poll.id, pollName: poll.name,
                pollType: poll.ptype, t: poll.yesno_poll_stats.total, pt: poll.yesno_poll_stats.participants, y: poll.yesno_poll_stats.yes,
                n: poll.yesno_poll_stats.no, u: poll.yesno_poll_stats.unknown});
        };

        $scope.downloadPoll = function (poll) {
            PollService.downloadPoll(poll).then(function(response) {
                var data = helpers.objArrayToCsv(response.data);
                var anchor = angular.element('<a/>');
                 anchor.attr({
                     href: 'data:attachment/csv;charset=utf-8,' + encodeURI(data),
                     target: '_blank',
                     download: 'poll-'+poll+'.csv'
                 })[0].click();

                anchor.remove();
                growl.success('Poll ['+poll+ '] downloaded successfully', {
                    ttl: 5000
                });

            });
        }

        $scope.notSorted = function(obj){
            if (!obj) {
                return [];
            }
            var sorted = Object.keys(obj);
            return sorted
        }

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
