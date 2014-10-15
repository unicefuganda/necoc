(function (module) {

    function Layer(map, layer, layerOptions) {
        var selected = false,
            layerStyle;

        function init(self) {
            layer
                .on('mouseover', self.highlight)
                .on('mouseout', self.unhighlight)
                .on('click', self.click);
        }

        this.click = function (clickHandler) {
            map.fitBounds(layer.getBounds())
            clickHandler && clickHandler();
        };

        this.highlight = function () {
            layer.setStyle(layerOptions.selectedLayerStyle);
            selected = true;
        };

        this.unhighlight = function () {
            layer.setStyle(layerStyle || layerOptions.districtLayerStyle);
            selected = false;
        };

        this.isHighlighted = function () {
            return selected;
        };

        this.setStyle = function (style) {
            layerStyle = style;
            layer.setStyle(style);
        };

        this.getCenter = function () {
            return layer.getBounds().getCenter();
        };

        init(this);
    }

    module.factory('LayerMap', function () {
        var layerList = {},
            layerGroups = {};

        return {
            addLayer: function (layer, layerName) {
                layerList[layerName] = layer;
            },
            getLayer: function (layerName) {
                return layerList[layerName];
            },
            getSelectedLayer: function () {
                var highlightedLayer = {};
                angular.forEach(layerList, function (layer, layerName) {
                    if (layer.isHighlighted()) {
                        highlightedLayer[layerName] = layer;
                    }
                });
                return highlightedLayer;
            },
            selectLayer: function (layerName) {
                layerList[layerName].highlight();
            },
            clickLayer: function (layerName) {
                layerList[layerName].click();
            },
            getLayers: function () {
                return layerList;
            },
            addLayerGroup: function (type, layerGroup) {
                layerGroups[type] = layerGroup;
            },
            getLayerGroup: function (type) {
                return layerGroups[type];
            }

        }
    });

    module.factory('MapService', function (GeoJsonService, MapConfig, LayerMap, StatsService) {
        var map;

        function initMap(elementId) {
            var map = L.map(elementId).setView([1.436, 32.884], 7);

            L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a>',
                maxZoom: 13,
                minZoom: 7
            }).addTo(map);

            map.on('zoomend', function () {
                var layerGroup = LayerMap.getLayerGroup('aggregate_stats');
                if (map.getZoom() < 9 && map.hasLayer(layerGroup)) {
                    map.removeLayer(layerGroup);
                } else if(map.getZoom() >= 9 && !map.hasLayer(layerGroup)) {
                    layerGroup && map.addLayer(layerGroup);
                }
            });

            return map;
        }

        function circleMarkerIcon(type, content) {
            return L.divIcon({
                iconSize: new L.Point(50, 50),
                className: type + '-aggregate-marker-icon',
                html: '<div>' + content + '</div>'
            });
        }

        function aggregateMarker(layer, aggregrateType, aggregateValue) {
            return new L.Marker(layer.getCenter(), {
                icon: circleMarkerIcon(aggregrateType, aggregateValue)
            })
        }

        function addAggregateLayer(map, parentLayerName) {
            var layerGroup = L.layerGroup();

            return StatsService.getAggregates().then(function (response) {
                var aggregateStats = response.data;
                var layer = LayerMap.getLayer(parentLayerName);

                if (aggregateStats[parentLayerName]) {
                    angular.forEach(aggregateStats[parentLayerName], function (aggregateValue, aggregateType) {
                        var marker = aggregateMarker(layer, aggregateType, aggregateValue.count);
                        layerGroup.addLayer(marker);
                    });
                    var savedGroup = LayerMap.getLayerGroup('aggregate_stats');
                    savedGroup && map.removeLayer(savedGroup);
                    LayerMap.addLayerGroup('aggregate_stats', layerGroup);
                    map.addLayer(layerGroup);
                }
            });
        }

        function addHeatMapLayer() {
            return StatsService.getAggregates().then(function (response) {
                var aggregateStats = response.data;

                angular.forEach(LayerMap.getLayers(), function (layer, layerName) {
                    if (aggregateStats[layerName]) {
                        layer.setStyle(MapConfig.heatMapStyle.messages(aggregateStats[layerName].messages.percentage))
                    } else {
                        layer.setStyle(MapConfig.heatMapStyle.messages(0))
                    }
                });
            })
        }

        function addDistrictsLayer(map) {
            return GeoJsonService.districts().then(function (response) {
                L.geoJson(response.data, {
                    style: MapConfig.districtLayerStyle,
                    onEachFeature: function (feature, layer) {
                        var districtLayer = new Layer(map, layer, MapConfig);
                        var districtName = feature.properties.DNAME_2010 || 'unknown';
                        LayerMap.addLayer(districtLayer, districtName.toLowerCase())
                    }
                }).addTo(map);
            });
        }

        return {
            render: function (elementId, layerName) {
                map = initMap(elementId);

                return addDistrictsLayer(map).then(function () {
                    layerName && map.setZoom(7) && this.selectLayer(layerName);
                }.bind(this)).then(function () {
                    addHeatMapLayer();
                }).then(function () {
                    return this;
                }.bind(this));
            },
            getZoom: function () {
                return map.getZoom();
            },
            setZoom: function (zoom) {
                return map.setZoom(zoom);
            },
            getCenter: function () {
                return map.getCenter();
            },
            highlightLayer: function (layerName) {
                LayerMap.selectLayer(layerName.toLowerCase());
            },
            getHighlightedLayer: function () {
                return LayerMap.getSelectedLayer();
            },
            selectLayer: function (layerName) {
                if (layerName) {
                    LayerMap.clickLayer(layerName.toLowerCase());
                    this.highlightLayer(layerName);
                    addAggregateLayer(map, layerName);
                }
            }
        };
    });

    module.directive('map', function (MapService, $window, $stateParams) {
        return {
            scope: false,
            link: function (scope, element, attrs) {
                MapService.render(attrs.id, $stateParams.district).then(function (map) {
                    $window.map = map;

                    scope.$watch('params.location', function (newLocation) {
                        newLocation && MapService.selectLayer(newLocation.district);
                    }, true);
                });
            }
        }
    });

})(angular.module('dms.map', ['dms.config', 'ui.router', 'dms.geojson', 'dms.stats']));