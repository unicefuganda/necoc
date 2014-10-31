(function (module) {

    module.controller('DashboardMessagesController', function ($scope, MessageService) {

        $scope.$watch('params.location', function (location) {
            $scope.district = (location && location.district) ? location.district : '';
            $scope.subcounty = (location && location.subcounty) ? location.subcounty : '';
        }, true);

        MessageService.all().then(function (response) {
            $scope.messages = response.data;
        });

        $scope.showMessageCheckboxes = false;
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

})(angular.module('dms.dashboard', ['dms.message']));
