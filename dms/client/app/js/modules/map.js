(function (module) {

    module.factory('MapService', function (GeoJsonService, MapConfig, LayerMap, StatsService, Layer, $interval, $chroma) {
        var map,
            self = this;

        var TOGGLE_ZOOM_LEVEL = 9;

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
                addLayerGroupOnZoom('aggregate_stats', TOGGLE_ZOOM_LEVEL);
                addLayerGroupOnZoom('sub_counties', TOGGLE_ZOOM_LEVEL);
                removeLayerGroupOnZoom('disaster_bubbles', TOGGLE_ZOOM_LEVEL);
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

        function addHeatMapLegend(map, stats) {
            var legend = L.control({position: MapConfig.legendPosition});

            legend.onAdd = function () {
                var div = L.DomUtil.create('div', 'info legend'),
                    scale = legendScale(stats),
                    intervals = 50;

                div.innerHTML += '<div class="legend-title"> Messages </div>';

                for (var i = 0; i < intervals; i++) {
                    div.innerHTML += '<div><span style="background:' + buildColor(Math.sqrt(i / intervals)) + '"></span>' +
                        (
                                i == 0 ? '<i>' + scale[0] + '</i>' :
                                i > ((intervals - 1) / 2) && i <= ((intervals) / 2) ? '<i>' + scale[1] + '</i>' :
                                i == (intervals - 1) ? '<i>' + scale[2] + '</i>' : ''
                            )
                        + '<div>';
                }
                return div;
            };

            try {
                LayerMap.getControl('legend').removeFrom(map);
            } catch (E) {
            }

            LayerMap.addControl('legend', legend);
            map.addControl(legend);
        }

        function legendScale(stats) {
            var scale = [0],
                maxMessages = messagesPeakValue(stats),
                median = Math.round(maxMessages / 2);

            if (maxMessages > 1 && maxMessages != median && median != 0) {
                scale.push(median);
                scale.push(maxMessages);
            } else {
                scale.push('');
                scale.push(1);
            }

            return scale;
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

        function addDisasterCountMarker(aggregateValue, layerGroup, childLayer) {
            if (aggregateValue.disasters.count > 0) {
                var disasterMarker = disastersAggregateMarker(childLayer, aggregateValue.disasters.count);
                layerGroup.addLayer(disasterMarker);
            }
        }

        function addMessagesCountMarker(aggregateValue, layerGroup, childLayer) {
            if (aggregateValue.messages.count > 0) {
                var messageMarker = messagesAggregateMarker(childLayer, aggregateValue.messages.count);
                layerGroup.addLayer(messageMarker);
            }
        }

        function addAggregateLayer(map, filter) {
            var layerGroup = L.layerGroup();

            return StatsService.getAggregates(filter).then(function (response) {
                var aggregateStats = response.data,
                    layer = LayerMap.getLayer(filter.district);

                angular.forEach(aggregateStats, function (aggregateValue, aggregateName) {
                    var childLayer = layer.getChildLayer(aggregateName);
                    if (childLayer) {
                        addMessagesCountMarker(aggregateValue, layerGroup, childLayer);
                        addDisasterCountMarker(aggregateValue, layerGroup, childLayer);
                    }
                });

                var savedGroup = LayerMap.getLayerGroup('aggregate_stats');
                try {
                    map.hasLayer(savedGroup) && map.removeLayer(savedGroup);
                } catch (err) {
                }
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
            var savedGroup = LayerMap.getLayerGroup('disaster_bubbles');
            map.hasLayer(savedGroup) && map.removeLayer(savedGroup);
            LayerMap.addLayerGroup('disaster_bubbles', layerGroup);
            map.addLayer(layerGroup);
        }

        function messagesPeakValue(stats) {
            if (!Object.keys(stats).length) {
                return 0;
            }

            var district = Object.keys(stats).reduce(function (prevDistrict, nextDistrict) {
                if (stats[prevDistrict].messages.count > stats[nextDistrict].messages.count) {
                    return prevDistrict;
                }
                return nextDistrict;
            });
            return stats[district].messages.count
        }

        function generateHeatMapColor(stats, layerName) {
            var maxMessages = messagesPeakValue(stats),
                scaleValue = 0;

            if (maxMessages != 0) {
                scaleValue = Math.sqrt((stats[layerName].messages.count) / maxMessages);
            }
            return buildColor(scaleValue);
        }

        function buildColor(scaleValue) {
            var scale = $chroma.scale(MapConfig.heatMapColors);
            return scale(scaleValue).hex();
        }

        function heatMapStyle(stats, layerName) {
            return {
                fillColor: generateHeatMapColor(stats, layerName),
                fillOpacity: 0.6,
                weight: 2
            }
        }

        function addHeatMapLayer(filter) {
            var filterCopy = angular.copy(filter);
            delete filterCopy.district;

            return StatsService.getAggregates(filterCopy).then(function (response) {
                var aggregateStats = response.data;

                angular.forEach(LayerMap.getLayers(), function (layer, layerName) {
                    if (aggregateStats[layerName]) {
                        layer.setStyle(heatMapStyle(aggregateStats, layerName));
                    } else {
                        layer.setStyle(MapConfig.heatMapColors[0]);
                    }
                });
                addHeatMapLegend(map, aggregateStats);
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
            render: function (elementId, district, subcounty, filter) {
                map = initMap(elementId);

                return addDistrictsLayer(map).then(function () {
                    var options = {animate: false};
                    if (district) {
                        this.selectDistrict(district, filter, options).then(function () {
                            this.selectSubcounty(district, subcounty);
                        }.bind(this));
                    }
                }.bind(this)).then(function () {
                    addHeatMapLayer(filter).then(addDisasterBubbles.bind({}, map)).then(function () {
                        removeLayerGroupOnZoom('disaster_bubbles', TOGGLE_ZOOM_LEVEL);
                    });
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
            selectDistrict: function (district, filter, options) {
                if (district) {
                    district = district.toLowerCase();
                    LayerMap.zoomIn(district, options);
                    this.highlightLayer(district);
                }

                return this.addSubCountyLayer(district).then(function () {
                    this.loadClusterLayer(filter, district);
                }.bind(this));
            },
            selectSubcounty: function (district, subcounty) {
                if (subcounty) {
                    var subCountyLayer = LayerMap.getLayer(district.toLowerCase()).getChildLayer(subcounty.toLowerCase());
                    subCountyLayer && subCountyLayer.zoomIn();
                }
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
            loadClusterLayer: function (filter, district) {
                filter ? filter.district = district.toLowerCase() :
                    filter = { district: district.toLowerCase() };
                addAggregateLayer(map, filter).then(function () {
                    addLayerGroupOnZoom('aggregate_stats', TOGGLE_ZOOM_LEVEL);
                });
            },
            numberOfLayersIn: function (layerGroupName) {
                return LayerMap.getLayerGroup(layerGroupName).getLayers().length;
            },
            refreshHeatMap: function (filter) {
                addHeatMapLayer(filter).then(addDisasterBubbles.bind({}, map)).then(function () {
                    removeLayerGroupOnZoom('disaster_bubbles', TOGGLE_ZOOM_LEVEL);
                });
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
                MapService.render(attrs.id, $stateParams.district, $stateParams.subcounty, scope.filter).then(function (map) {
                    $window.map = map;

                    map.onClickDistrict(function (district) {
                        $state.go('admin.dashboard.district', {district: district}, {reload: false}).then(function () {
                            MapService.selectDistrict(district, scope.filter);
                        });
                    });

                    map.onClickSubcounty(function (subcounty) {
                        $state.go('admin.dashboard.district.subcounty', {subcounty: subcounty}, {reload: false}).then(function () {
                            var district = $stateParams.district;
                            MapService.selectSubcounty(district, subcounty);
                        });
                    });

                    $interval(function () {
                        map.refreshHeatMap(scope.filter);
                    }, 15000);

                    scope.$watch('filter', function (filter) {
                        if (filter) {
                            map.refreshHeatMap(filter);
                            $stateParams.district && map.loadClusterLayer(filter, $stateParams.district);
                        }
                    }, true);
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
                                MapService.selectDistrict(district, scope.filter);
                            });

                    } else {
                        $state.go('admin.dashboard', {}, {reload: true});
                    }
                });
            }
        }
    });

})(angular.module('dms.map', ['dms.config', 'ui.router', 'dms.geojson', 'dms.stats', 'dms.layer', 'dms.utils']));
