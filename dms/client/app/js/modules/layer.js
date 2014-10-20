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
                layerList[layerName] && layerList[layerName].highlight();
            },
            clickLayer: function (layerName) {
                layerList[layerName] && layerList[layerName].click();
                layerList[layerName] && layerList[layerName].zoomIn();
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