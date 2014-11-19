(function (module) {

    module.constant('Config', {
        baseUrl: window.location.origin,
        apiUrl: window.location.origin + "/api/v1/",
        districtsGeoJsonUrl: window.location.origin + '/static/map_data/uganda_districts_2011_geo.json',
        geoServerUrl: 'http://ec2-54-218-182-219.us-west-2.compute.amazonaws.com/geoserver/geonode/ows' +
            '?service=WFS&version=1.0.0&request=GetFeature&outputFormat=json',
        exportPollUrl: window.location.origin + '/export/poll-responses/'
    });

    module.constant('MapConfig', {
        maxBubbleRadius: 50,
        disasterBubbleStyle: {
            radius: 0,
            color: '#FC4F55',
            fillOpacity: 0.4,
            weight: 1,
            clickable: false
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
        heatMapColors: [
            '#DFFF67',
            '#FEE629',
            '#FAAE22',
            '#FB8E1F',
            '#EF2602'
        ]
    });

    module.constant('Permissions', {
        LIST: [
            'can_manage_users',
            'can_manage_polls',
            'can_view_polls',
            'can_manage_disasters',
            'can_manage_messages'
        ]
    });

})(angular.module('dms.config', []));
