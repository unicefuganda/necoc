(function (module) {

    function messagesHeatMapColor(p) {
        return p > 100 ? '#BD0026' :
                p > 80 ? '#E31A1C' :
                p > 60 ? '#FC4E2A' :
                p > 40 ? '#FD8D3C' :
                p > 20 ? '#FEB24C' :
                p > 0 ? '#FED976' :
            '#FFEDA0';
    }

    module.constant('Config', {
        baseUrl: window.location.origin,
        apiUrl: window.location.origin + "/api/v1/",
        districtsGeoJsonUrl: window.location.origin + '/static/map_data/uganda_districts_2011_geo.json',
        geoServerUrl: 'http://ec2-54-218-182-219.us-west-2.compute.amazonaws.com/geoserver/geonode/ows' +
            '?service=WFS&version=1.0.0&request=GetFeature&outputFormat=json'
    });

    module.constant('MapConfig', {
        maxBubbleRadius: 50,
        disasterBubbleStyle: {
            radius: 0,
            color: '#FC4F55',
            fillOpacity: 0.4,
            weight: 1,
            clickable : false
        },
        legendPosition: 'bottomleft',
        districtLayerStyle: {
            weight: 2,
            color: "#3E9CB8",
            fillColor: "#eee",
            fillOpacity: 0.2,
            opacity: 0.7
        },
        selectedLayerStyle: {
            weight: 4,
            fillOpacity: 0.7
        },
        heatMapStyle: {
            messages: function (percentage) {
                return {
                    fillColor: messagesHeatMapColor(percentage),
                    fillOpacity: 0.6,
                    weight: 2
                }
            }
        }
    });

})(angular.module('dms.config', []));