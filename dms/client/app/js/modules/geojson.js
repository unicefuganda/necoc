(function (module) {

    module.factory('GeoJsonService', function ($http, Config) {

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
            url += filter ? '&filter=' + filterQuery(filter) + '&callback=JSON_CALLBACK' : '';
            return url;
        }

        return {

            districts: function () {
                return $http.get(Config.districtsGeoJsonUrl, {cache: true});
            },

            subCounties: function (district) {
                var propertyNames = ['the_geom', "DNAME_2010", 'SNAME_2010'];
                var filter = { 'DNAME_2010': district.toUpperCase() };
                return $http.jsonp(geoServerUrlFilter('subcounties_2011_0005', filter, propertyNames), {cache: true});
            }
        }
    });

})(angular.module('dms.geojson', ['dms.config']));