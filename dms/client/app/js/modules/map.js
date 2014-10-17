(function (module) {

    module.factory('Layer', function () {

        function Layer(layerName, map, layer, options) {
            var selected = false,
                layerStyle,
                name = layerName.toLowerCase();

            function init(self) {
                layer
                    .on('mouseover', self.highlight)
                    .on('mouseout', self.unhighlight)
                    .on('click', self.click);
            }

            this.getName = function () {
                return name;
            };

            this.getStyle = function () {
                return layerStyle;
            };

            this.zoomIn = function () {
                map.fitBounds(layer.getBounds());
            };

            this.click = function () {
                options.onClickHandler && options.onClickHandler(name)
            };

            this.highlight = function () {
                layer.setStyle(options.style.selectedLayerStyle);
                selected = true;
            };

            this.unhighlight = function () {
                layer.setStyle(layerStyle || options.style.districtLayerStyle);
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

        return {
            build: function (layerName, map, layer, options) {
                return new Layer(layerName, map, layer, options);
            }
        }
    });

    module.factory('LayerMap', function () {
        var layerList = {},
            layerGroups = {};

        return {
            addLayer: function (layer) {
                layerList[layer.getName()] = layer;
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
            highlightLayer: function (layerName) {
                layerList[layerName].highlight();
            },
            clickLayer: function (layerName) {
                layerList[layerName].click();
                layerList[layerName].zoomIn();
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

    module.factory('MapService', function (GeoJsonService, MapConfig, LayerMap, StatsService, Layer) {
        var map,
            self = this;

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
                } else if (map.getZoom() >= 9 && !map.hasLayer(layerGroup)) {
                    layerGroup && map.addLayer(layerGroup);
                }
            });

            return map;
        }

        function addHeatMapLegend(map) {
            var legend = L.control({position: MapConfig.legendPosition});

            legend.onAdd = function () {
                var div = L.DomUtil.create('div', 'info legend'),
                    scale = [0, 20, 40, 60, 80, 100];
                div.innerHTML += '<div class="legend-title">Legend</div>';

                for (var i = 0; i < scale.length - 1 ; i++) {
                    div.innerHTML += '<i style="background:' + MapConfig.heatMapStyle.messages(scale[i] + 1).fillColor + '"></i> ' +
                        scale[i] + (scale[i + 1] ? '&ndash;' + scale[i + 1] + ' % <br>' : '+');
                }
                return div;
            };
            legend.addTo(map);
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

        function addHeatMapLayer(map) {
            return StatsService.getAggregates().then(function (response) {
                var aggregateStats = response.data;

                angular.forEach(LayerMap.getLayers(), function (layer, layerName) {
                    if (aggregateStats[layerName]) {
                        layer.setStyle(MapConfig.heatMapStyle.messages(aggregateStats[layerName].messages.percentage));
                    } else {
                        layer.setStyle(MapConfig.heatMapStyle.messages(0));
                    }
                });

                addHeatMapLegend(map);
            });
        }

        function addDistrictsLayer(map) {
            self.districtlayerOptions = {
                style: MapConfig
            };

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

        return {
            render: function (elementId, layerName) {
                map = initMap(elementId);

                return addDistrictsLayer(map).then(function () {
                    layerName && map.setZoom(7) && this.selectLayer(layerName);
                }.bind(this)).then(function () {
                    addHeatMapLayer(map);
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
                LayerMap.highlightLayer(layerName.toLowerCase());
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
            },
            onClickDistrict: function (handler) {
                self.districtlayerOptions.onClickHandler = handler;
            }
        };
    });

    module.directive('map', function (MapService, $window, $stateParams, $state) {
        return {
            scope: false,
            link: function (scope, element, attrs) {
                MapService.render(attrs.id, $stateParams.district).then(function (map) {
                    $window.map = map;

                    scope.$watch('params.location', function (newLocation) {
                        newLocation && MapService.selectLayer(newLocation.district);
                    }, true);

                    map.onClickDistrict(function (district) {
                        $state.go('admin.dashboard.district', {district: district});
                    })
                });
            }
        }
    });

})(angular.module('dms.map', ['dms.config', 'ui.router', 'dms.geojson', 'dms.stats']));