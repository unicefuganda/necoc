(function (module) {

    module.factory('CoordinatesService', function ($http, Config) {

        return {
            getCoordinates: function () {
                return $http.get(Config.apiUrl + 'current-coordinates/');
            }
        };
    });

})(angular.module('dms.coordinates', ['dms.config']));
