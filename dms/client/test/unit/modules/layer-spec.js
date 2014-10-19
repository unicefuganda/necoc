describe('dms.layer', function () {

    beforeEach(function () {
        module('dms.layer');
    });

    describe('LayerMap', function () {
        var layerMap,
            layer,
            mapMock,
            mapLayerMock,
            mockBounds = [2, 4];

        beforeEach(function () {
            mapMock = jasmine.createSpyObj('mapMock', ['fitBounds']);
            mapLayerMock = jasmine.createSpyObj('mapLayerMock', ['on', 'setStyle', 'getBounds']);
            mapLayerMock.on.andReturn(mapLayerMock);
            mapLayerMock.getBounds.andReturn(mockBounds);

            inject(function (LayerMap, Layer) {
                layerMap = LayerMap;
                layer = Layer;
            });
        });

        it('should add a layer to the layerlist', function () {
            var builtLayer = layer.build('lira', mapMock, mapLayerMock, {});
            layerMap.addLayer(builtLayer);
            expect(layerMap.getLayer(builtLayer.getName())).toEqual(builtLayer);
        });

        it('should get selected layer from layersList', function () {
            var layerA = layer.build('bukoto', mapMock, mapLayerMock, {style: {}});
            var layerB = layer.build('naguru', mapMock, mapLayerMock, {});
            layerA.highlight();

            layerMap.addLayer(layerA);
            layerMap.addLayer(layerB);
            expect(layerMap.getSelectedLayer()).toEqual({ bukoto: layerA });
        });

        it('should highlight a layer', function () {
            var builtLayer = layer.build('lira', mapMock, mapLayerMock, {style: {}});
            layerMap.addLayer(builtLayer);

            layerMap.highlightLayer(builtLayer.getName());
            expect(builtLayer.isHighlighted()).toBeTruthy();
        });

        it('should click a layer', function () {
            var mockOptions = jasmine.createSpyObj('mockOptions', ['onClickHandler']);
            var builtLayer = layer.build('lira', mapMock, mapLayerMock, mockOptions);
            layerMap.addLayer(builtLayer);

            layerMap.clickLayer(builtLayer.getName());
            expect(mockOptions.onClickHandler).toHaveBeenCalledWith('lira');
            expect(mapMock.fitBounds).toHaveBeenCalledWith(mockBounds);
        });

        it('should check if a layer exists', function () {
            var builtLayer = layer.build('lira', mapMock, mapLayerMock, {});
            layerMap.addLayer(builtLayer);

            expect(layerMap.hasLayer('lira')).toBeTruthy();
            expect(layerMap.hasLayer('gulu')).toBeFalsy();
        });

        it('should get layers hash', function () {
            expect(layerMap.getLayers()).toEqual({});

            var builtLayer = layer.build('lira', mapMock, mapLayerMock, {});
            layerMap.addLayer(builtLayer);

            expect(layerMap.getLayers()).toEqual({lira: builtLayer});
        });

        it('should add a layer and retrieve group', function () {
            var stubLayerGroup = { name: 'layer-group'};
            layerMap.addLayerGroup(stubLayerGroup.name, stubLayerGroup);
            expect(layerMap.getLayerGroup(stubLayerGroup.name)).toEqual(stubLayerGroup);
        });
    });
});