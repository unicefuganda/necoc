describe('dms.map', function () {

    beforeEach(function () {
        module('dms.map');
    });

    describe('LayerMap', function () {
        var layerMap;
        beforeEach(function () {
            inject(function (LayerMap) {
                layerMap = LayerMap;
            });
        });

        it('should add a layer to the layerlist', function () {
            var layer = {'name': "Bukoto"};
            layerMap.addLayer(layer, layer.name);
            expect(layerMap.getLayer(layer.name)).toEqual(layer);
        });

        it('should get selected layer from layersList', function () {
            var layerA = {'name': "Bukoto", isHighlighted: function () {
                return true;
            }};

            var layerB = {'name': "Naguru", isHighlighted: function () {
                return false;
            }};

            layerMap.addLayer(layerA, layerA.name);
            layerMap.addLayer(layerB, layerB.name);

            expect(layerMap.getSelectedLayer()).toEqual({ Bukoto: layerA });
        });

        it('should select a layer', function () {
            var layer = jasmine.createSpyObj('layer', ['highlight']);
            layer.name = 'Bukoto';

            layerMap.addLayer(layer, layer.name);
            layerMap.selectLayer(layer.name);
            expect(layer.highlight).toHaveBeenCalled();
        });

        it('should click a layer', function () {
            var layer = jasmine.createSpyObj('layer', ['click']);
            layer.name = 'Bukoto';

            layerMap.addLayer(layer, layer.name);
            layerMap.clickLayer(layer.name);
            expect(layer.click).toHaveBeenCalled();
        });

    });
});