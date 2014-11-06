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
            if(!filter) return;

            var newFilter = angular.copy(filter);
            newFilter.to ? newFilter.to = addDay(newFilter.to): null;

            MessageService.filter(newFilter).then(function (response) {
                $scope.messages = response.data;
            });
        }, true);

        $scope.showMessageCheckboxes = false;

        function addDay(date) {
            return $moment(date, 'YYYY-MM-DD').add(1, 'days').format('YYYY-MM-DD');
        }
    });

    module.directive('slidingPanel', function () {
        return {
            link: function (scope, element, attrs) {
                var showing = true,
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
                        element.animate({left: '26%'});
                    }
                    showing = !showing;
                }
            }
        }
    })

})(angular.module('dms.dashboard', ['dms.message', 'dms.utils']));
