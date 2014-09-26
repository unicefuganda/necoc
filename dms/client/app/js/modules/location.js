(function (module) {

    module.factory('LocationService', function ($http, Config) {
        return {
            districts: function () {
                return $http.get(Config.apiUrl + 'locations/?type=district');
            }
        };
    });

    module.directive('selectLocation', function (LocationService) {
       return {
           link: function (scope, element) {
                element.selectize({
                    valueField: 'id',
                    labelField: 'name',
                    searchField: 'name',
                    maxItems: 1,
                    create: false,
                    preload: true,
                    load: function (query, callback) {
                        LocationService.districts().then(function (response) {
                            callback(response.data)
                        });
                    }
                });
           }
       }
    });

})(angular.module('dms.location', ['dms.config']));
