(function (module) {

    module.factory('Layer', function () {

        function Layer(layerName, map, mapLayer, options) {
            var selected = false,
                layer = mapLayer,
                layerStyle,
                name = layerName.toLowerCase();

            var children = {};

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

            this.zoomIn = function (options) {
                map.fitBounds(layer.getBounds(), options);
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

            this.addChildLayer = function (layer) {
                children[layer.getName()] = layer
            };

            this.getChildLayer = function (layerName) {
                return children[layerName];
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
                layerList[layerName] && layerList[layerName].highlight();
            },
            clickLayer: function (layerName) {
                var layer = layerList[layerName];
                if (layer) {
                    layer.click();
                }
            },
            zoomIn: function (layerName, options) {
                var layer = layerList[layerName];
                if (layer) {
                    layer.zoomIn(options);
                }
            },
            hasLayer: function (layerName) {
                return layerList[layerName] ? true : false;
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

})(angular.module('dms.layer', []));