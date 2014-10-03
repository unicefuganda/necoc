(function (module) {


    module.factory('DisasterTypeService', function ($http, Config) {
        return {
            all: function () {
                return $http.get(Config.apiUrl + 'disaster-types/');
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
                    create: false,
                    preload: true,
                    load: function (query, callback) {
                        DisasterTypeService.all().then(function (response) {
                            callback(response.data)
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
