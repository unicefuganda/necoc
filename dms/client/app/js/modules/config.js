(function (module) {

    function geoserverHost() {
        if (window.location.origin.match(/localhost/)) {
            return 'http://178.62.69.21:8080/'
        }
        return window.location.origin + ':8080/'
    }

    module.constant('Config', {
        baseUrl: window.location.origin,
        apiUrl: window.location.origin + "/api/v1/",
        districtsGeoJsonUrl: window.location.origin + '/static/map_data/uganda_districts_2011_geo.json',
        geoServerUrl: geoserverHost() + 'geoserver/wfs?service=WFS&version=1.0.0&request=GetFeature' +
            '&outputFormat=text/javascript',
        exportPollUrl: window.location.origin + '/export/poll-responses/'
    });

    module.constant('DisasterConfig', {
        statuses: ['Registered', 'Situation Report Field', 'Verification', 'Assessment', 'Deployed Response Team', 'Closed']
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
        messageClusterColor: 'rgba(28, 177, 105, 0.6)',
        disasterClusterColor: 'rgba(232, 84, 91, 0.6)',
        heatMapLegendPosition: 'bottomleft',
        clusterLegendPosition: 'bottomleft',
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
        ],
        enablePrinting: false
    });

    module.constant('Permissions', {
        LIST: [
            'can_manage_users',
            'can_manage_polls',
            'can_view_polls',
            'can_view_messages',
            'can_view_disasters',
            'can_manage_disasters',
            'can_manage_messages'
        ]
    });

    module.constant('ChartConfig', {
        chart: {
            type: 'pie',
            plotBackgroundColor: '#3E9CB8',
            backgroundColor: '#3E9CB8',
            borderWidth: 0,
            plotBorderWidth: null,
            plotShadow: false
        },
        tooltip: {
            formatter: function () {
                return '<b>' + this.point.name + '</b>: ' + this.y.toFixed(1);
            }
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: false
                },
                showInLegend: true
            }
        },

        legend: {
            enabled: true,
            align: 'right',
            layout: 'vertical',
            verticalAlign: 'middle',
            itemStyle: {'color': '#3E9CB8'},
            backgroundColor: 'white'
        },
        colors: ['#90ed7d', '#8085e9', '#f15c80', '#e4d354', '#8085e8', '#8d4653', '#91e8e1', '#7cb5ec', '#434348', '#f7a35c']
    });

})(angular.module('dms.config', []));
