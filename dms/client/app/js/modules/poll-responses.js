(function (module) {

    module.factory('PollResponsesService', function ($http, Config) {
        return {
            all: function () {
                return $http.get(Config.apiUrl + 'poll-responses/');
            },
            filter: function (filter, filter_id) {
                return $http.get(Config.apiUrl + 'poll-responses/?' + filter + '=' + filter_id);
            },
            uncategorized: function() {
                return $http.get(Config.apiUrl + 'poll-responses/?uncategorized=True');
            }
        }
    });

    module.controller('PollResponsesController', function ($scope, PollResponsesService, $stateParams, $state, Config, helpers) {
        var poll_id = $stateParams.poll;
        $scope.ptype = $stateParams.pollType;
        $scope.ysCount = { 'pt': $stateParams.pt, 'total': $stateParams.t, 'yes': $stateParams.y, 'no': $stateParams.n , 'unknown': $stateParams.u  };
        console.log($scope.ysCount)
        $scope.export_poll_response_url = Config.exportPollUrl;

        $scope.isYesnoPoll = function () {
            return ($scope.ptype == 'yesno') ? true : false;
        }

        setScopeData = function(resp_data){
            $scope.response_data = resp_data;
        }

        if (poll_id) {
            PollResponsesService.filter('poll', poll_id).then(function (response) {
                $scope.poll_responses = response.data;
                $scope.poll_text = $stateParams.pollName;
            });
            $scope.export_poll_response_url += poll_id + '/';
        }

        $scope.backToPolls = function () {
            $state.go('admin.polls');
        };

        $scope.uncategorizedResponses = function () {
            PollResponsesService.uncategorized().then(function(response){
                $scope.poll_responses = response.data;
            });
        };

        $scope.chartConfig = {
            options: {
                chart: {
                    plotBackgroundColor: null,
                    plotBorderWidth: null,
                    plotShadow: false,
                    type: 'pie'
                }
            },
            title: {
                text: $stateParams.pollName + ' :Poll Results Analysis'
            },
            tooltip: {
                pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
            },
            plotOptions: {
                pie: {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    dataLabels: {
                        enabled: false
                    },
                    showInLegend: true
                }
            },
            loading: false,
            series: [{
                name: 'Poll',
                colorByPoint: true,
                data: [{
                    name: 'NO',
                    y: parseInt($scope.ysCount.no)
                }, {
                    name: 'YES',
                    y: parseInt($scope.ysCount.yes),
                    sliced: true,
                    selected: true
                }, {
                    name: 'Uknown',
                    y: parseInt($scope.ysCount.unknown)
                }]
            }]
        }

        $scope.notSorted = function(obj){
            if (!obj) {
                return [];
            }
            var sorted = Object.keys(obj);
            return sorted
        }

    });

})(angular.module('dms.poll-responses', ['dms.config', 'ui.router', 'highcharts-ng', 'dms.utils']));
