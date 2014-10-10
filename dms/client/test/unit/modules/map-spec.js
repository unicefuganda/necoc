describe('dms.map', function () {

    beforeEach(function () {
        module('dms.map');
    });

    describe('GeoJsonService', function () {

        var httpMock,
            districtsGeoJsonUrl,
            geoJsonService,
            districtsGeoJsonStub = {
                type: "Feature",
                geometry: {
                    type: "Point",
                    coordinates: [125.6, 10.1]
                },
                properties: {
                    name: "Dinagat Islands"
                }
            };

        beforeEach(function () {

            inject(function (GeoJsonService, Config, $httpBackend) {
                httpMock = $httpBackend;
                geoJsonService = GeoJsonService;
                districtsGeoJsonUrl = Config.districtsGeoJsonUrl;
                httpMock.when('GET', districtsGeoJsonUrl).respond(districtsGeoJsonStub);
            });
        });

        describe('GeoJsonService.district', function(){
            it('should fetch districts GeoJSON', function(){
                var obtainedGeoJson = geoJsonService.districts();
                httpMock.expectGET(districtsGeoJsonUrl);
                httpMock.flush();
                expect(obtainedGeoJson).toBeDefined();
            });
        });


    });

});