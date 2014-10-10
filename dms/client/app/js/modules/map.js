(function (module) {

    module.factory('GeoJsonService', function ($http, Config) {
        return {
            districts: function(){
                return $http.get(Config.districtsGeoJsonUrl);
            }
        }
    });

    module.factory('MapService', function (GeoJsonService, MapConfig) {
        var map;

        function initMap(elementId) {
            if (!map) {
                map = L.map(elementId).setView([1.436, 32.884], 7);

                L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a>',
                    maxZoom: 13,
                    minZoom:7
                }).addTo(map);


            }
            return map;
        };

        function addDistrictsLayer(){
            GeoJsonService.districts().then(function(response){
                L.geoJson(response.data, {
                    style: MapConfig.districtLayerStyle
                }).addTo(map);
            });
        };


        return {
            render: function (elementId) {
                initMap(elementId);
                addDistrictsLayer();
            }
        };
    });

    module.directive('map', function (MapService) {
        return {
            link: function (scope, element, attrs) {
                MapService.render(attrs.id);
            }
        }
    });

})(angular.module('dms.map', ['dms.config']));