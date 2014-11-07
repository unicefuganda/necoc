(function (module) {


    module.factory('StatsService', function ($http, Config, helpers) {

        return {
            getAggregates: function (statOptions) {
                var options = statOptions || {};
                var location = options.location;
                delete options.location;
                var queryString = helpers.buildQueryString(options);
                if (location) {
                    return $http.get(Config.apiUrl + 'location-stats/' + location + '/' + queryString);
                }
                return $http.get(Config.apiUrl + 'location-stats/' + queryString);
            }
        };
    });

})(angular.module('dms.stats', ['dms.config', 'dms.utils']));
