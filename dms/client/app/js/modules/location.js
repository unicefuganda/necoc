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
           link: function (scope, element, attrs) {
                var $select = element.selectize({
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

               scope.$watch(attrs.selectLocation, function (user) {
                    if (!user) {
                        var selectize = $select[0].selectize;
                        selectize.clear();
                    }
               });
           }
       }
    });

})(angular.module('dms.location', ['dms.config']));
