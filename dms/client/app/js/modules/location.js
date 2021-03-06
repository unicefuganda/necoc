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

    module.directive('locationCascade', function (LocationService, helpers, $q) {
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
                            loadParentOptions(attrs.locationCascade, query, callback);
                        }
                    },
                    onChange: function (value) {
                        if (attrs.child && value) {
                            scope.select[attrs.child].load(loadChildOptions.bind({}, attrs.child, value));
                        }
                    }
                });

                function loadChildOptions(type, input, callback) {
                    var locationIds = helpers.stringToArray(input, ','),
                        locationPromises = locationIds.map(function (id) {
                            return LocationService[type](id);
                        });

                    $q.all(locationPromises).then(function (responses) {
                        var options = responses.reduce(function (accumulator, response) {
                            return accumulator.concat(response.data);
                        }, []);
                        scope.select[type].clearOptions();
                        callback(options);
                        var defaultValue = scope.$eval(attrs.defaultChildValue);
                        if (defaultValue) {
                            if (defaultValue.indexOf(",") > -1) {
                                scope.select[type].setValue(helpers.stringToArray(defaultValue, ','));
                            } else {
                                scope.select[type].setValue(defaultValue);
                            }
                        }
                        scope.$watch(attrs.defaultChildValue, function (defaultChildValue) {
                            if (defaultChildValue) {
                                if (defaultChildValue.indexOf(",") > -1) {
                                    scope.select[type].setValue(helpers.stringToArray(defaultChildValue, ','));
                                } else {
                                    scope.select[type].setValue(defaultChildValue);
                                }
                            }
                        });
                    });
                }

                function loadParentOptions(type, input, callback) {
                    LocationService[type](input).then(function (response) {
                        callback(response.data);
                        var defaultValue = scope.$eval(attrs.defaultParentValue);
                        if (defaultValue) {
                            $select[0].selectize.setValue(defaultValue);
                        }
                        scope.$watch(attrs.defaultParentValue, function (defaultParentValue) {
                            if (defaultParentValue) {
                                $select[0].selectize.setValue(defaultParentValue);
                            }
                        });
                    });
                }

                scope.select[attrs.locationCascade] = $select[0].selectize;

                scope.$watch(attrs.dataset, function (dataSet) {
                    if (!dataSet || Object.keys(dataSet).length == 0) {
                        scope.select[attrs.locationCascade].clear();
                    }
                }, true);
            }
        }
    });

})(angular.module('dms.location', ['dms.config', 'dms.utils']));
