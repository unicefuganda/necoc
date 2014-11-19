(function (module) {


    module.factory('DisasterTypeService', function ($http, Config) {
        return {
            all: function () {
                return $http.get(Config.apiUrl + 'disaster-types/');
            },
            create: function (disasterType) {
                return $http.post(Config.apiUrl + 'disaster-types/', disasterType);
            }
        }
    });

    module.directive('disasterTypes', function (DisasterTypeService) {
        return {
            link: function (scope, element, attrs) {
                var $select = element.selectize({
                    valueField: 'id',
                    labelField: 'name',
                    searchField: 'name',
                    maxItems: 1,
                    preload: true,
                    load: function (query, callback) {
                        DisasterTypeService.all().then(function (response) {
                            callback(response.data)
                            scope.$watch(attrs.defaultValue, function (defaultValue) {
                                if (defaultValue) {
                                    $select[0].selectize.setValue(defaultValue);
                                }
                            });
                        });
                    },
                    create: function (input, callback) {
                        DisasterTypeService.create({name: input})
                            .then(function (response) {
                                callback(response.data)
                            }, function () {
                                callback(false);
                            });
                    }
                });

                scope.$watch(attrs.disasterTypes, function (user) {
                    if (!user) {
                        $select[0].selectize.clear();
                    }
                });
            }
        }
    });

})(angular.module('dms.disaster-type', ['dms.config']));
