(function (module) {

    module.factory('MapService', function (GeoJsonService, MapConfig, LayerMap, StatsService, Layer, $interval) {
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
                addLayerGroupOnZoom('aggregate_stats', 9);
                addLayerGroupOnZoom('sub_counties', 9);
                removeLayerGroupOnZoom('disaster_bubbles', 9);
            });
        }

        function addLayerGroupOnZoom(layerGroupName, zoomLevel) {
            var layerGroup = LayerMap.getLayerGroup(layerGroupName);

            if (map.getZoom() < zoomLevel && map.hasLayer(layerGroup)) {
                layerGroup && map.removeLayer(layerGroup);
            } else if (map.getZoom() >= zoomLevel && !map.hasLayer(layerGroup)) {
                layerGroup && map.addLayer(layerGroup);
            }
        }

        function removeLayerGroupOnZoom(layerGroupName, zoomLevel) {
            var layerGroup = LayerMap.getLayerGroup(layerGroupName);

            if (map.getZoom() < zoomLevel && !map.hasLayer(layerGroup)) {
                layerGroup && map.addLayer(layerGroup);
            } else if (map.getZoom() >= zoomLevel && map.hasLayer(layerGroup)) {
                layerGroup && map.removeLayer(layerGroup);
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

        function circleMarkerIcon(content, classPrefix) {
            return L.divIcon({
                iconSize: new L.Point(40, 40),
                className: classPrefix + '-aggregate-marker-icon',
                html: '<div>' + content + '</div>'
            });
        }

        function aggregateMarker(layer, aggregateValue, classPrefix) {
            return new L.Marker(layer.getCenter(), {
                icon: circleMarkerIcon(aggregateValue, classPrefix)
            });
        }

        function messagesAggregateMarker(layer, count) {
            return aggregateMarker(layer, count, 'messages');
        }

        function disastersAggregateMarker(layer, count) {
            return aggregateMarker(layer, count, 'disasters');
        }

        function addAggregateLayer(map, parentLayerName) {
            var layerGroup = L.layerGroup();

            return StatsService.getAggregates(parentLayerName).then(function (response) {
                var aggregateStats = response.data,
                    layer = LayerMap.getLayer(parentLayerName);

                angular.forEach(aggregateStats, function (aggregateValue, aggregateName) {
                    var childLayer = layer.getChildLayer(aggregateName);
                    if (childLayer) {
                        var messageMarker = messagesAggregateMarker(childLayer, aggregateValue.messages.count);
                        var disasterMarker = disastersAggregateMarker(childLayer, aggregateValue.disasters.count);
                        layerGroup.addLayer(messageMarker);
                        layerGroup.addLayer(disasterMarker);
                    }
                });

                var savedGroup = LayerMap.getLayerGroup('aggregate_stats');
                map.hasLayer(savedGroup) && map.removeLayer(savedGroup);
                LayerMap.addLayerGroup('aggregate_stats', layerGroup);
                map.addLayer(layerGroup);
            });
        }

        function animate(circleMarker, percentage) {
            var radius = 0,
                maxRadius = parseInt((percentage * MapConfig.maxBubbleRadius) / 100);

            $interval(function () {
                radius < maxRadius ? radius += (maxRadius / MapConfig.maxBubbleRadius) : radius = 0;
                circleMarker.setRadius(radius);
            }, 50);
        }

        function disasterBubble(latLng, percentage) {
            var circleMarker = new L.CircleMarker(latLng, MapConfig.disasterBubbleStyle);
            animate(circleMarker, percentage);
            return circleMarker;
        }

        function addDisasterBubbles(map, aggregateStats) {
            var layerGroup = L.layerGroup();

            angular.forEach(aggregateStats, function (aggregateValue, aggregateName) {
                var layer = LayerMap.getLayer(aggregateName);
                if (layer && aggregateValue.disasters.percentage) {
                    var bubble = disasterBubble(layer.getCenter(), aggregateValue.disasters.percentage);
                    layerGroup.addLayer(bubble);
                }
            });

            LayerMap.addLayerGroup('disaster_bubbles', layerGroup);
            map.addLayer(layerGroup);
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
                return aggregateStats;
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
                    }
                });
                var existingLayerGroup = LayerMap.getLayerGroup('sub_counties');
                map.hasLayer(existingLayerGroup) && map.removeLayer(existingLayerGroup);
                LayerMap.addLayerGroup('sub_counties', layerGroup);
                map.addLayer(layerGroup);
            });
        }

        return {
            render: function (elementId, district, subcounty) {
                map = initMap(elementId);

                return addDistrictsLayer(map).then(function () {
                    var options = {animate: false};
                    if (district) {
                        this.selectDistrict(district, options).then(function () {
                            this.selectSubcounty(district, subcounty);
                        }.bind(this));
                    }
                }.bind(this)).then(function () {
                    addHeatMapLayer().then(addDisasterBubbles.bind({}, map));
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
            selectDistrict: function (layerName, options) {
                if (layerName) {
                    layerName = layerName.toLowerCase();
                    LayerMap.zoomIn(layerName, options);
                    this.highlightLayer(layerName);
                }

                return this.addSubCountyLayer(layerName).then(function () {
                    addAggregateLayer(map, layerName.toLowerCase());
                });
            },
            selectSubcounty: function (district, subcounty) {
                var subCountyLayer = LayerMap.getLayer(district.toLowerCase()).getChildLayer(subcounty.toLowerCase());
                subCountyLayer && subCountyLayer.zoomIn();
            },
            addSubCountyLayer: function (district) {
                return addSubCountyLayer(district);
            },
            onClickDistrict: function (handler) {
                self.districtlayerOptions.onClickHandler = handler;
            },
            onClickSubcounty: function (handler) {
                self.subCountyLayerOptions.onClickHandler = handler;
            },
            numberOfLayersIn: function (layerGroupName) {
                return LayerMap.getLayerGroup(layerGroupName).getLayers().length;
            },
            refreshHeatMap: function () {
                addHeatMapLayer();
            },
            clickSubCounty: function (district, subcounty) {
                return LayerMap.getLayer(district.toLowerCase()).getChildLayer(subcounty.toLowerCase()).click();
            }
        };
    });

    module.directive('map', function (MapService, $window, $stateParams, $state, $interval) {
        return {
            scope: false,
            link: function (scope, element, attrs) {
                MapService.render(attrs.id, $stateParams.district, $stateParams.subcounty).then(function (map) {
                    $window.map = map;

                    map.onClickDistrict(function (district) {
                        $state.go('admin.dashboard.district', {district: district}, {reload: false}).then(function () {
                            MapService.selectDistrict(district);
                        });
                    });

                    map.onClickSubcounty(function (subcounty) {
                        $state.go('admin.dashboard.district.subcounty', {subcounty: subcounty}, {reload: false}).then(function () {
                            var district = $stateParams.district;
                            MapService.selectSubcounty(district, subcounty);
                        });
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
                                MapService.selectDistrict(district);
                            });

                    } else {
                        $state.go('admin.dashboard', {}, {reload: true});
                    }
                });
            }
        }
    });

})(angular.module('dms.map', ['dms.config', 'ui.router', 'dms.geojson', 'dms.stats', 'dms.layer']));
