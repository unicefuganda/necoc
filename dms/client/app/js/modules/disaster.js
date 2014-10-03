(function (module) {

    module.factory('DisasterService', function ($http, Config, $moment) {
        return {
            create: function (disaster) {
                disaster.date = $moment(disaster.date, "YYYY/MM/DD hh:mm").format('YYYY-MM-DDTHH:mm');
                return $http.post(Config.apiUrl + 'disasters/', disaster);
            },
            all: function () {
                return $http.get(Config.apiUrl + 'disasters/');
            }
        };
    });

    module.controller('DisastersController', function ($scope, DisasterService) {
        DisasterService.all().then(function (response) {
            $scope.disasters = response.data;
        });
    });

    module.controller('DisastersModalController', function ($scope, DisasterService) {
        $scope.saveDisaster = function () {
            if ($scope.disasters_form.$valid) {
                $scope.saveStatus = true;

                DisasterService.create($scope.disaster).then(function (response) {
                    $scope.disaster = null;
                    $scope.saveStatus = false;
                    $scope.disasters.push(response.data);
                });

            } else {
                $scope.hasErrors = true;
            }
        }
    });

    module.directive('disasterStatus', function () {
        return {
            link: function (scope, element, attrs) {
                var $select = element.selectize({
                    valueField: 'value',
                    labelField: 'name',
                    searchField: 'name',
                    maxItems: 1,
                    create: false,
                    preload: true,
                    options: [
                        {value: 'Assessment', name: 'Assessment'},
                        {value: 'Response Team Deployed', name: 'Response Team Deployed'},
                        {value: 'Closed', name: 'Closed'},
                    ]
                });

                scope.$watch(attrs.disasterStatus, function (disaster) {
                    if (!disaster) {
                        $select[0].selectize.clear();
                    }
                });
            }
        }
    })


})(angular.module('dms.disaster', ['dms.config', 'dms.utils']));
