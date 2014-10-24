(function (module) {


    module.factory('StatsService', function ($http, Config) {

        return {
            getAggregates: function (locationName) {
                if (locationName) {
                    return $http.get(Config.apiUrl + 'location-stats/' + locationName + '/');
                }
                return $http.get(Config.apiUrl + 'location-stats/');
            }
        };
    });

})(angular.module('dms.stats', ['dms.config']));
