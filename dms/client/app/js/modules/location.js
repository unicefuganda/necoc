(function (module) {

    module.factory('LocationService', function ($http, Config) {
        return {
            districts: function () {
                return $http.get(Config.apiUrl + 'locations/?type=district', { cache: true });
            },
            subcounties: function (districtId) {
                return $http.get(Config.apiUrl + 'locations/?district=' + districtId + '&type=subcounty', { cache: true });
            }
        };
    });

    module.directive('selectLocation', function (LocationService) {
        return {
            link: function (scope, element, attrs) {
                var $select = element.selectize({
                    valueField: 'id',
                    labelField: 'name',
                    searchField: 'name',
                    maxItems: parseInt(attrs.maxLocations) || null,
                    create: false,
                    preload: true,
                    load: function (query, callback) {
                        LocationService.districts().then(function (response) {
                            callback(response.data)
                        });
                    }
                });

                scope.$watch(attrs.selectLocation, function (user) {
                    if (!user) {
                        var selectize = $select[0].selectize;
                        selectize.clear();
                    }
                });
            }
        }
    });

    module.directive('locationCascade', function (LocationService) {
        return {
            scope: false,
            controller: function ($scope) {
                if (!$scope.select) {
                    $scope.$parent.select = {};
                }
            },
            link: function (scope, element, attrs) {

                var $select = element.selectize({
                    valueField: 'id',
                    labelField: 'name',
                    searchField: 'name',
                    maxItems: parseInt(attrs.maxLocations) || null,
                    create: false,
                    preload: true,
                    load: function (query, callback) {
                        if (attrs.parent) {
                            loadOptions(attrs.locationCascade, query, callback);
                        }
                    },
                    onChange: function (value) {
                        if (attrs.child && value) {
                            console.log(attrs.child);
                            scope.select[attrs.child].load(loadOptions.bind({}, attrs.child, value));
                        }
                    }
                });

                function loadOptions(type, input, callback) {
                    LocationService[type](input).then(function (response) {
                        scope.select[type].clearOptions();
                        callback(response.data);
                    });
                }

                scope.select[attrs.locationCascade] = $select[0].selectize;

                scope.$watch(attrs.dataSet, function (dataSet) {
                    if (!dataSet) {
                        scope.select[attrs.locationCascade].clear();
                    }
                });
            }
        }
    });

})(angular.module('dms.location', ['dms.config']));
