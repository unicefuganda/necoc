(function (module) {

    module.controller('DashboardController', function ($rootScope, $moment) {
        $rootScope.filter = { from: yesterday() };

        function yesterday() {
            return $moment().subtract(1, 'days').format('YYYY-MM-DD')
        }
    });

    module.controller('DashboardMessagesController', function ($rootScope, $scope, MessageService, $moment) {

        $scope.$watch('params.location', function (location) {
            $scope.district = (location && location.district) ? location.district : '';
            $scope.subcounty = (location && location.subcounty) ? location.subcounty : '';
        }, true);

        $rootScope.$watch('filter', function (filter) {
            if (!filter) return;

            var newFilter = angular.copy(filter);
            newFilter.to ? newFilter.to = addDay(newFilter.to) : null;
            if (!newFilter.disaster_type) delete newFilter.disaster_type;

            MessageService.filter(newFilter).then(function (response) {
                $scope.messages = response.data;
            });
        }, true);

        $scope.showMessageCheckboxes = false;

        function addDay(date) {
            return $moment(date, 'YYYY-MM-DD').add(1, 'days').format('YYYY-MM-DD');
        }
    });

    module.controller('DashboardStatsController', function ($rootScope, $scope, StatsSummaryService, $moment, ChartConfig) {
        $scope.locationTitles = {};
        $scope.disasterTypeDistribution = [];
        $scope.series = [];

        function summaryStatsTitle(location) {
            var locationTitleMapping = {district: 'District', subcounty: 'Subcounty'},
                subLocationTitleMapping = {district: 'Subcounties', subcounty: 'Subcounty'};

            $scope.locationTitles.name = 'Uganda';
            $scope.locationTitles.subLocation = 'Districts';

            angular.forEach(location, function (value, key) {
                $scope.locationTitles.name = value.toUpperCase() + ' ' + locationTitleMapping[key];
                $scope.locationTitles.subLocation = subLocationTitleMapping[key];
            });
        }

        function addDay(date) {
            return $moment(date, 'YYYY-MM-DD').add(1, 'days').format('YYYY-MM-DD');
        }

        function clean(newFilter) {
            newFilter.to ? newFilter.to = addDay(newFilter.to) : null;
            !newFilter.disaster_type ? delete newFilter.disaster_type : null;
        }

        function toArray(data) {
            var arr = [];
            angular.forEach(data, function (value, key) {
                arr.push([key, value]);
            });
            return arr;
        }

        function updateStats(filter) {
            if (!filter) return;

            var newFilter = angular.copy(filter);
            clean(newFilter);

            StatsSummaryService.getSummary(newFilter).then(function (response) {
                $scope.stats = response.data;
                $scope.disasterTypeDistribution = toArray(response.data.disasters.types);
                $scope.series[0] = {data: $scope.disasterTypeDistribution};
            });
        }

        $scope.$watch('params.location', function (location) {
            summaryStatsTitle(location);

            if (location && location.subcounty) {
                var newFilter = angular.copy($scope.filter);
                newFilter.subcounty = location.subcounty;
                updateStats(newFilter);
            }

        }, true);

        $rootScope.$watch('filter', updateStats, true);

        $scope.disasterStatsCharts = {
            options: ChartConfig,
            title: {
                text: ''
            },
//            size: {width: 450, height: 450},
            series: $scope.series
        };

    });

    module.directive('slidingPanel', function () {
        return {
            link: function (scope, element, attrs) {
                var showing = true,
                    openAnimate = {message: '26%', stats: '70%'},
                    chevron = element.find('.' + attrs.slidingPanel);

                togglePanel();
                chevron.on('click', togglePanel);

                function togglePanel() {
                    if (showing) {
                        chevron.removeClass('icon-chevron-right-1')
                            .addClass('icon-chevron-left');
                        element.animate({left: '97%'});
                    } else {
                        chevron.removeClass('icon-chevron-left')
                            .addClass('icon-chevron-right-1');
                        element.animate({left: openAnimate[attrs.for]});
                    }
                    showing = !showing;
                }
            }
        }
    });

})
(angular.module('dms.dashboard', ['dms.message', 'dms.utils', 'highcharts-ng', 'dms.config']));
