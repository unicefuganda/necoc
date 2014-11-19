(function (module) {


    module.factory('StatsService', function ($http, Config, helpers) {

        return {
            getAggregates: function (statOptions) {
                var options = angular.copy(statOptions || {});
                var district = options.district;
                delete options.district;
                var queryString = helpers.buildQueryString(options);
                if (district) {
                    return $http.get(Config.apiUrl + 'location-stats/' + district + '/' + queryString);
                }
                return $http.get(Config.apiUrl + 'location-stats/' + queryString);
            }
        };
    });

    module.factory('StatsSummaryService', function ($http, Config, helpers) {
        return {
            getSummary: function (statOptions) {
                var queryString = helpers.buildQueryString(statOptions);
                return $http.get(Config.apiUrl + 'stats-summary/' + queryString);
            }
        };
    });

})(angular.module('dms.stats', ['dms.config', 'dms.utils']));
