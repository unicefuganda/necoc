(function (module) {

    module.factory('GeoJsonService', function ($http, Config, $q) {

        function filterQuery(filter) {
            var query = '<Filter xmlns="http://www.opengis.net/ogc">';
            for (var key in filter) {
                query += "<PropertyIsEqualTo>" +
                    "<PropertyName>" + key + "</PropertyName>" +
                    "<Literal>" + filter[key] + "</Literal>" +
                    "</PropertyIsEqualTo>";
            }
            query += "</Filter>";
            return query;
        }

        function geoServerUrlFilter(dataset, filter, propertyNames) {
            var url = Config.geoServerUrl + '&typeName=geonode:' + dataset;
            url += propertyNames ? '&propertyName=' + propertyNames.join(',') : '';
            url += filter ? '&filter=' + filterQuery(filter) + '&format_options=callback:JSONPCallback' : '';
            return url;
        }

        return {

            districts: function () {
                return $http.get(Config.districtsGeoJsonUrl, {cache: true});
            },

            subCounties: function (district) {
                var deferred = $q.defer();
                JSONPCallback = function (data) {
                    deferred.resolve(data);
                };
                var propertyNames = ['the_geom', "DNAME_2010", 'SNAME_2010'],
                    filter = { 'DNAME_2010': district.toUpperCase() },
                    url = geoServerUrlFilter('subcounties_2011_0005', filter, propertyNames);

                $http.jsonp(url, {cache: true});

                return deferred.promise;
            }
        }
    });

})(angular.module('dms.geojson', ['dms.config']));