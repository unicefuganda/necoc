(function (module) {

    module.factory('MapService', function (GeoJsonService, MapConfig, LayerMap, StatsService, Layer) {
        var map,
            self = this;

        self.subCountyLayerOptions = { style: MapConfig };
        self.districtlayerOptions = { style: MapConfig };

        function initMap(elementId) {
            var map = L.map(elementId).setView([1.436, 32.884], 7);

            L.tileLayer('http://otile{s}.mqcdn.com/tiles/1.0.0/map/{z}/{x}/{y}.png', {
                attribution: 'Map data Tiles &copy; <a href="http://www.mapquest.com/" target="_blank">MapQuest</a> <img src="http://developer.mapquest.com/content/osm/mq_logo.png" />',
                subdomains: '1234',
                maxZoom: 13,
                minZoom: 7
            }).addTo(map);

            initMapEvents(map);
            return map;
        }

        function initMapEvents(map) {
            map.on('zoomend', function () {
                toggleLayerGroupOnZoom('aggregate_stats', 9);
                toggleLayerGroupOnZoom('sub_counties', 9);
            });
        }

        function toggleLayerGroupOnZoom(layerGroupName, zoomLevel) {
            var layerGroup = LayerMap.getLayerGroup(layerGroupName);

            if (map.getZoom() < zoomLevel && map.hasLayer(layerGroup)) {
                map.removeLayer(layerGroup);
            } else if (map.getZoom() >= zoomLevel && !map.hasLayer(layerGroup)) {
                layerGroup && map.addLayer(layerGroup);
            }
        }

        function addHeatMapLegend(map) {
            var legend = L.control({position: MapConfig.legendPosition});

            legend.onAdd = function () {
                var div = L.DomUtil.create('div', 'info legend'),
                    scale = [0, 20, 40, 60, 80, 100];
                div.innerHTML += '<div class="legend-title">Legend</div>';

                for (var i = 0; i < scale.length - 1; i++) {
                    div.innerHTML += '<i style="background:' + MapConfig.heatMapStyle.messages(scale[i] + 1).fillColor + '"></i> ' +
                        scale[i] + (scale[i + 1] ? '&ndash;' + scale[i + 1] + ' % <br>' : '+');
                }
                return div;
            };
            legend.addTo(map);
        }

        function circleMarkerIcon(type, content, classPrefix) {
            return L.divIcon({
                iconSize: new L.Point(40, 40),
                className: classPrefix + '-aggregate-marker-icon',
                html: '<div>' + content + '</div>'
            });
        }

        function aggregateMarker(layer, aggregrateName, aggregateValue, classPrefix) {
            return new L.Marker(layer.getCenter(), {
                icon: circleMarkerIcon(aggregrateName, aggregateValue, classPrefix)
            });
        }

        function messagesAggregateMarker(layer, aggregateName, count) {
            return aggregateMarker(layer, aggregateName, count, 'messages');
        }

        function addAggregateLayer(map, parentLayerName) {
            var layerGroup = L.layerGroup();

            return StatsService.getAggregates(parentLayerName).then(function (response) {
                var aggregateStats = response.data,
                    layer = LayerMap.getLayer(parentLayerName);

                angular.forEach(aggregateStats, function (aggregateValue, aggregateName) {
                    var childLayer = layer.getChildLayer(aggregateName);
                    if (childLayer) {
                        var marker = messagesAggregateMarker(childLayer, aggregateName, aggregateValue.messages.count);
                        layerGroup.addLayer(marker);
                    }
                });

                var savedGroup = LayerMap.getLayerGroup('aggregate_stats');
                savedGroup && map.removeLayer(savedGroup);
                LayerMap.addLayerGroup('aggregate_stats', layerGroup);
                map.addLayer(layerGroup);
            });
        }

        function addHeatMapLayer() {
            return StatsService.getAggregates().then(function (response) {
                var aggregateStats = response.data;

                angular.forEach(LayerMap.getLayers(), function (layer, layerName) {
                    if (aggregateStats[layerName]) {
                        layer.setStyle(MapConfig.heatMapStyle.messages(aggregateStats[layerName].messages.percentage));
                    } else {
                        layer.setStyle(MapConfig.heatMapStyle.messages(0));
                    }
                });
            });
        }

        function addDistrictsLayer(map) {
            return GeoJsonService.districts().then(function (response) {
                L.geoJson(response.data, {
                    style: MapConfig.districtLayerStyle,
                    onEachFeature: function (feature, layer) {
                        var districtName = feature.properties.DNAME_2010 || 'unknown',
                            districtLayer = Layer.build(districtName, map, layer, self.districtlayerOptions);
                        LayerMap.addLayer(districtLayer);
                    }
                }).addTo(map);
            });
        }

        function addSubCountyLayer(district) {
            var layerGroup = L.layerGroup();

            return GeoJsonService.subCounties(district).then(function (data) {
                L.geoJson(data, {
                    style: MapConfig.districtLayerStyle,
                    onEachFeature: function (feature, layer) {
                        var subCountyName = feature.properties.SNAME_2010 || 'unknown',
                            subCountyLayer = Layer.build(subCountyName, map, layer, self.subCountyLayerOptions);
                        LayerMap.getLayer(district).addChildLayer(subCountyLayer);
                        layerGroup.addLayer(layer);
                        console.log(subCountyName);
                    }
                });
                LayerMap.addLayerGroup('sub_counties', layerGroup);
                map.addLayer(layerGroup);
            });
        }

        return {
            render: function (elementId, layerName) {
                map = initMap(elementId);

                return addDistrictsLayer(map).then(function () {
                    layerName && map.setZoom(7) && this.selectLayer(layerName);
                }.bind(this)).then(function () {
                    addHeatMapLayer();
                    addHeatMapLegend(map);
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
            hasLayer: function (layerName) {
                return LayerMap.hasLayer(layerName);
            },
            highlightLayer: function (layerName) {
                LayerMap.highlightLayer(layerName.toLowerCase());
            },
            getHighlightedLayer: function () {
                return LayerMap.getSelectedLayer();
            },
            selectLayer: function (layerName) {
                if (layerName) {
                    layerName = layerName.toLowerCase();
                    LayerMap.zoomIn(layerName);
                    this.highlightLayer(layerName);
                    this.addSubCountyLayer(layerName).then(function() {
                        addAggregateLayer(map, layerName.toLowerCase());
                    });
                }
            },
            addSubCountyLayer: function (district) {
                var layerGroup = LayerMap.getLayerGroup('sub_counties');
                map.hasLayer(layerGroup) && map.removeLayer(layerGroup);
                return addSubCountyLayer(district);
            },
            onClickDistrict: function (handler) {
                self.districtlayerOptions.onClickHandler = handler;
            },
            refreshHeatMap: function () {
                addHeatMapLayer();
            }
        };
    });

    module.directive('map', function (MapService, $window, $stateParams, $state, $interval) {
        return {
            scope: false,
            link: function (scope, element, attrs) {
                MapService.render(attrs.id, $stateParams.district).then(function (map) {
                    $window.map = map;

                    map.onClickDistrict(function (district) {
                        $state.go('admin.dashboard.district', {district: district}, {reload: false});
                        MapService.selectLayer(district);
                    });

                    $interval(function () {
                        map.refreshHeatMap();
                    }, 15000);
                });
            }
        }
    });

    module.directive('searchMap', function ($state, MapService) {
        return {
            scope: false,
            link: function (scope, element, attrs) {

                scope.$watch(attrs.ngModel, function (district) {
                    if (district == undefined) return;

                    if (district) {
                        MapService.hasLayer(district.toLowerCase()) &&
                        $state.go('admin.dashboard.district', {district: district.toLowerCase()}, {reload: true})
                            .then(function () {
                                MapService.selectLayer(district);
                            });

                    } else {
                        $state.go('admin.dashboard', {}, {reload: true});
                    }
                });
            }
        }
    });

})(angular.module('dms.map', ['dms.config', 'ui.router', 'dms.geojson', 'dms.stats', 'dms.layer']));
