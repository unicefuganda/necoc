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


    describe('Layer', function () {
        var mockMapLayer,
            mockMap,
            layer;

        beforeEach(function () {
            mockMap = jasmine.createSpyObj('mockMap', ['fitBounds', 'removeLayer']);
            mockMapLayer = jasmine.createSpyObj('mockMapLayer', ['on', 'setStyle', 'getBounds']);
            mockMapLayer.on.andReturn(mockMapLayer);

            inject(function (LayerMap, Layer) {
                layer = Layer;
            });
        });

        describe('METHOD: addChildLayer', function () {
            it('should add child layer to a parent layer', function () {
                var subCountyLayer = layer.build('lira-sub-county', mockMap, mockMapLayer, {});
                var districtLayer = layer.build('lira-district', mockMap, mockMapLayer, {});

                districtLayer.addChildLayer(subCountyLayer);
                expect(districtLayer.getChildLayer('lira-sub-county')).toEqual(subCountyLayer);
            });
        });

        describe('METHOD: getName', function () {
            it('should return a layer name', function () {
                var districtLayer = layer.build('lira-district', mockMap, mockMapLayer, {});
                expect(districtLayer.getName()).toEqual('lira-district');
            });
        });

        describe('METHOD: setStyle', function () {
            it('should set a layer style', function () {
                var style = {color: 'red'};
                var districtLayer = layer.build('lira-district', mockMap, mockMapLayer, {});
                districtLayer.setStyle(style);
                expect(mockMapLayer.setStyle).toHaveBeenCalledWith(style);
                expect(districtLayer.getStyle()).toEqual(style);
            });
        });

        describe('METHOD: zoomIn', function () {
            it('should zoom into a certain layer', function () {
                var mockBounds = [12.3, 23.4];
                mockMapLayer.getBounds.andReturn(mockBounds);
                var districtLayer = layer.build('lira-district', mockMap, mockMapLayer, {});

                districtLayer.zoomIn();
                expect(mockMap.fitBounds).toHaveBeenCalledWith(mockBounds);
            });
        });

        describe('METHOD: click', function () {
            it('should call the on click handler of a layer', function () {
                var optionsMock = jasmine.createSpyObj('optionsMock', ['onClickHandler']),
                    districtLayer = layer.build('lira-district', mockMap, mockMapLayer, optionsMock);

                districtLayer.click();
                expect(optionsMock.onClickHandler).toHaveBeenCalledWith('lira-district');
            });
        });

        describe('METHOD: highlight', function () {
            it('should highlight layer', function () {
                var optionsMock = jasmine.createSpyObj('optionsMock', ['onClickHandler']);
                optionsMock.style = { selectedLayerStyle: { color: 'red'} };
                var districtLayer = layer.build('lira-district', mockMap, mockMapLayer, optionsMock);

                districtLayer.highlight();
                expect(mockMapLayer.setStyle).toHaveBeenCalledWith({ color: 'red'});
                expect(districtLayer.isHighlighted()).toBeTruthy();
            });
        });

        describe('METHOD: getCenter', function () {
            it('should get the center of a layer', function () {
                var mockBounds = jasmine.createSpyObj('mockBounds', ['getCenter']);
                mockMapLayer.getBounds.andReturn(mockBounds);
                var districtLayer = layer.build('lira-district', mockMap, mockMapLayer, {});

                districtLayer.getCenter();
                expect(mockMapLayer.getBounds).toHaveBeenCalled();
                expect(mockBounds.getCenter).toHaveBeenCalled();
            });
        });

    });
});