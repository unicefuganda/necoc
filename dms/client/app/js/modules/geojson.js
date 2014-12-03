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
            var url = Config.geoServerUrl + '&typeNames=subcounties:' + dataset;
            url += propertyNames ? '&propertyName=' + propertyNames.join(',') : '';
            url += filter ? '&filter=' + filterQuery(filter) : '';
            url += '&format_options=callback:JSON_CALLBACK';
            return url;
        }

        return {

            districts: function () {
                return $http.get(Config.districtsGeoJsonUrl, {cache: true});
            },

            subCounties: function (district) {
                var propertyNames = ["the_geom","DNAME2014", 'SNAME2014'],
                    filter = { DNAME2014: district.toUpperCase() },
                    url = geoServerUrlFilter('UGANDA_SUBCOUNTIES_2014', filter, propertyNames);
                return $http.jsonp(url, {cache: true});
            }
        }
    });

})(angular.module('dms.geojson', ['dms.config']));