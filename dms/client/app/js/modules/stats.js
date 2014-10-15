(function (module) {


    module.factory('StatsService', function ($http, Config) {
        return {
            getAggregates: function () {
                return $http.get(Config.apiUrl + 'location-stats')
            }
        };
    });

})(angular.module('dms.stats', ['dms.config']));
